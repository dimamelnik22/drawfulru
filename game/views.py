from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from game.models import PhrasePack, Phrase, PlayedGame, Image, OnlineGame, Round, PlayersChoice, PlayersNewPhrase
from user_profile.models import Profile
from .forms import RoundResultFull, RoundResultScoreOnly, LoginForm, UserRegisterForm, ChooseAnswer
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
import random
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import requests


# Create your views here.
def home_view(request):
	games = OnlineGame.objects.all()
	if request.method == 'POST':
		newPack = PhrasePack()
		newPack.title = "randomaddedbybutton"+str(datetime.datetime.now())
		newPack.save()
		newPack.phrases.set(Phrase.objects.order_by('?')[:8])
		newPack.save()		
		return redirect('game-home')
	player = "unnamed"
	if request.user.is_active:
		player = Profile.objects.get(user = request.user)
		if not player:
			player = "unnamed"
		else:
			player = player.name
	return render(request, 'game/home.html', context={'games': games,'data':PhrasePack.objects.all(),'name': player})

def auth_view(request):
	return render(request,'game/auth.html')

def number_view(request):
	profiles = Profile.objects.all()
	form = LoginForm(request.POST or None)
	p = request.user.profile
	if p.number != None:
				return redirect('game-home')
	if form.is_valid():
		p.number = form.cleaned_data['name']
		p.save()
		return redirect('game-home')
	return render(request,'game/number.html', context={'form':form})

def nick_view(request):
	
	profiles = Profile.objects.all()
	for p in profiles:
		if request.user.id == p.user.id:
			
			return redirect('game-number')
	form = LoginForm(request.POST or None)
	if form.is_valid():
		profile = Profile()
		profile.name = form.cleaned_data['name']
		profile.user = request.user
		profile.save()
		return redirect('game-number')
	return render(request,'game/nick.html', context={'form':form})

def login_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        
        profile = Profile()
        profile.user = user
        profile.save()
        return redirect('game-home')
    return render(request, 'game/login.html', {'form': form})

def room_view(request,packid):

	game = OnlineGame()
	game.save()
	game.players.add(Profile.objects.get(user = request.user))
	game.phrasePack = PhrasePack.objects.get(id = packid)
	game.save()
	# pl = request.user.profile.name
	# pp = game.phrasePack.title
	# rate = game.phrasePack.rating
	# for p in Profile.objects.all():
	# 	phone = p.number
	# 	if len(phone) == 12:
	
	# 		data = {
	# 			'phoneNumber': phone,
	# 			'message': f'New game started! Host: {pl}. Phrase pack: {pp}. Rating: {rate}'
	# 		}
	# 		response = requests.post('https://ixl8j3vad0.execute-api.us-east-1.amazonaws.com/myNewStage/userinfo', json=data, headers={'Content-type': 'application/json'})
		
	return redirect("game-roomjoin", gameid=game.id)
	#return render(request, 'game/room.html', context={'phrases':game.phrasePack.phrases.all(), 'players':game.players, 'name':Profile.objects.get(user = request.user).name})

def roomjoin_view(request,gameid):
	game = OnlineGame.objects.get(id = gameid)
	if not game.players.filter(user = request.user):
		game.players.add(Profile.objects.get(user = request.user))
		game.save()
	if (game.players.all().count() >= 2) and game.players.all()[0].user == request.user and not game.isStarted:
		game.isStarted = True
		for index,pl in enumerate(game.players.all()):

			ground = Round()
			ground.player = pl
			ground.save()
			nphrase = Phrase()
			nphrase.gamesCount = -1
			nphrase.name = game.phrasePack.phrases.all()[index].name
			nphrase.author = pl
			nphrase.save()
			ground.phrases.add(nphrase)
			ground.save()
			game.rounds.add(ground)
			game.save()
	
	return render(request, 'game/room.html', context={'game':game,'phrases':game.phrasePack.phrases.all(), 'players':game.players.all(), 'name':Profile.objects.get(user = request.user).name})


@csrf_exempt
def lobby_view(request,gameid):
	cplayer = request.user.profile
	cplayer.waitingFor = 0
	cplayer.save()
	game = OnlineGame.objects.get(id = gameid)
	roundid = game.rounds.all()[0].id
	if request.method == 'GET':
		player = Profile.objects.get(user = request.user)
		ground = game.rounds.get(player = player)
		phrase = ground.phrases.all()[0]
		return render(request, 'game/lobby.html', context={'roundid':roundid,'phrase':phrase,'game':game,'rounds':game.rounds.all(),'players':game.players.all(), 'name':Profile.objects.get(user = request.user).name})
	elif request.method == 'POST':
		data = request.POST['save_cdata']
		image = request.POST['save_image']
		file_data = Image( image=data, canvas_image=image)
		file_data.save()
		player = Profile.objects.get(user = request.user)
		ground = game.rounds.get(player = player)
		ground.image = file_data
		ground.save()
		return redirect('/room/'+str(game.id)+'/suggest/')
	



def suggesting_view(request,gameid,roundid):
	game = OnlineGame.objects.get(id = gameid)

	player = Profile.objects.get(user = request.user)
	if request.method == 'GET':
		player.waitingFor +=1
		player.save()
	if game.curround >= game.rounds.count():
		return render(request,'game/allresult.html', context={'game':game})
	ground = game.rounds.get(id = roundid)
	if ground.player == player:
		return render(request, 'game/suggesting.html', context={'game':game, 'image':ground.image.image, 'roundid':roundid})
	form = LoginForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		phrase = Phrase()
		phrase.name = form.cleaned_data['name']
		phrase.author = Profile.objects.get(user = request.user)
		phrase.gamesCount = -1
		newPhrase = PlayersNewPhrase()
		
		phrase.save()
		newPhrase.player = phrase.author
		newPhrase.ground = ground
		newPhrase.newPhrase = phrase
		newPhrase.save()
		return redirect('/room/'+str(game.id)+'/wait/'+str(roundid)+'/guess')
		#return wait_view(request,game.id,roundid,'guess')
		#return render(request, 'game/suggesting.html', context={'game':game, 'image':ground.image.image, 'roundid':roundid})
	return render(request, 'game/suggesting.html', context={'game':game, 'image':ground.image.image, 'roundid':roundid,'form':form})

def guessing_view(request,gameid,roundid):
	game = OnlineGame.objects.get(id = gameid)
	player = Profile.objects.get(user = request.user)
	
	ground = game.rounds.get(id = roundid)
	form = ChooseAnswer(request.POST or None)
	if request.user.profile == game.players.all()[0]:
		for np in PlayersNewPhrase.objects.filter(ground = ground):
			ground.phrases.add(np.newPhrase)
			ground.save()
			np.delete()

		phrases = ground.phrases.order_by('?')[:8]
		ground.phrases.set(phrases)
		ground.save()
	phrases = ground.phrases.all()
	if request.method == 'GET':
		player.waitingFor +=1
		player.save()

	if ground.player == player:

		return render(request, 'game/guessing.html', context={'game':game, 'image':ground.image.image,'phrases':ground.phrases.all(), 'roundid':roundid})
	if request.method == 'POST' and form.is_valid():
		index = form.cleaned_data['Your_Choice']-1
		
		phrase = ground.phrases.all()[index]
		choice = PlayersChoice()
		choice.player = request.user.profile
		choice.chosenPhrase = phrase
		choice.ground = ground
		choice.save()

		return redirect('/room/'+str(game.id)+'/wait/'+str(roundid)+'/result')
		#return wait_view(request,game.id,roundid,'result')
		#return render(request, 'game/guessing.html', context={'game':game, 'image':ground.image.image,'phrases':ground.phrases.all(), 'roundid':roundid})
	return render(request, 'game/guessing.html', context={'form':form,'game':game, 'image':ground.image.image,'phrases':phrases, 'roundid':roundid})

def result_view(request,gameid,roundid):
	game = OnlineGame.objects.get(id = gameid)
	player = Profile.objects.get(user = request.user)

	if request.method == 'GET':
		player.waitingFor+=1
		player.save()
	tphrase = game.phrasePack.phrases.all()[game.curround]
	ground = game.rounds.get(id = roundid)
	if not ground.finished:
		for pc in PlayersChoice.objects.filter(ground=ground):
			phrase = pc.chosenPhrase
			phrase.rating = float(phrase.rating) + 1.0
			phrase.save()
			pc.delete()
		for p in ground.phrases.all():
			p.author.score += p.rating
			p.author.save()
		game.curround +=1
		game.save()
		ground.finished = True
		ground.save()
	
	


	
	if game.curround < game.rounds.count():
		roundid = game.rounds.all()[game.curround].id		
	return render(request, 'game/result.html', context={'tphrase':tphrase,'phrases':ground.phrases.all(), 'image':ground.image.image, 'roundid':roundid, 'game':game})

def wait_view(request,gameid,roundid,nextstage):
	game = OnlineGame.objects.get(id = gameid)
	player = Profile.objects.get(user = request.user)
	ready = False
	for p in game.players.all():
		if p.waitingFor > player.waitingFor:
			ready = True
	if request.user.profile == game.players.all()[0]:
		equal = True
		for p in game.players.all():
			if p.waitingFor != request.user.profile.waitingFor:
				equal = False
		if equal:
			ready = True


	return render(request, 'game/wait.html', context = {'ready':ready,'game':game, 'next':nextstage, 'roundid':roundid, 'player':player})

def end_view(request,gameid):
	if OnlineGame.objects.filter(id = gameid):
		game = OnlineGame.objects.get(id = gameid)
		if request.user.profile == game.players.all()[0]:
			
			# text = ""
			# sum = 0
			# for r in game.rounds.all():
			# 	text+=str(r.phrases.get(author = request.user.profile).rating)+" , "
			# 	sum+=r.phrases.get(author = request.user.profile).rating
			# phone = request.user.profile.number
			# if len(phone) == 12:
			# 	data = {
			# 		'phoneNumber': phone,
			# 		'message': f'Nice Game! Your rezults: {text} Total: {sum}'
			# 	}
			# 	response = requests.post('https://ixl8j3vad0.execute-api.us-east-1.amazonaws.com/myNewStage/userinfo', json=data, headers={'Content-type': 'application/json'})
			# 	print(response)
			newPack = []
			for r in game.rounds.all():
				if len(r.phrases.all()) > 0:
					phrase = r.phrases.order_by('-rating')[0]

					if game.phrasePack.phrases.filter(name = phrase.name):
						sphrase = game.phrasePack.phrases.get(name = phrase.name)
						if sphrase.gamesCount >= 10 :
							sphrase.rating = float(sphrase.rating)*0.9+float(phrase.rating)*0.1
						else:
							sphrase.rating = (sphrase.rating*sphrase.gamesCount+float(phrase.rating))/(sphrase.gamesCount+1)
						sphrase.gamesCount += 1
						sphrase.save()
						if len(r.phrases.all())>1:
							if r.phrases.order_by('-rating')[1].rating > 0:
								phrase = r.phrases.order_by('-rating')[1]

					name = phrase.name
					author = phrase.author
					rating = phrase.rating
					for p in r.phrases.all():
						p.delete() 

					if not Phrase.objects.filter(name = name):
						phrase = Phrase()
						phrase.name = name
						phrase.author = author
						phrase.save()
						author.numOfAuthoredPhrases+=1
						author.save()
					else:
						phrase = Phrase.objects.get(name = name)
					newPack.append(phrase)
					r.image.delete()
					r.delete()
			for p in game.players.all():
				p.score = 0
				p.save()
			for i in range(len(newPack),8):
				newPack.append(game.phrasePack.phrases.all()[i])
			pp = PhrasePack()
			pp.title = 'fromgame'+str(datetime.datetime.now())
			pp.save()
			pp.phrases.set(newPack)
			pp.save()
			game.phrasePack.gamesCount+=1
			game.phrasePack.save()
			game.delete()
	return redirect('game-home')


def anot():
	rounds = 8
	players = 8
	forms = []
	for i in range(rounds):
		forms.append([])
		forms[i].append("Фраза раунда: " + PhrasePack.objects.get(id = packid).phrases.all()[i].name)
		forms[i].append(RoundResultScoreOnly(request.POST or None, prefix = str(i)))
		for j in range(players-1):

			forms[i].append(RoundResultFull(request.POST or None, prefix = str(i)+str(j)))



	if request.method == 'POST':
		newPackPhrases = []
		phraseSuccess = 0
		packRating = 0
		game = PlayedGame()
		game.save()
		playerslist = Profile.objects.all()
		game.players.set(playerslist.exclude(user = User.objects.get(username = "dimme")))
		game.phrasePack = PhrasePack.objects.get(id = packid)
		game.save()
		for i in range(rounds):
			
			sphrase = []
			if forms[i][1].is_valid():
				packRating += forms[i][1].cleaned_data['score']
				sphrase = PhrasePack.objects.get(id = packid).phrases.all()[i]
				if sphrase.gamesCount >= 10 :
					sphrase.rating = float(sphrase.rating)*0.9+forms[i][1].cleaned_data['score']*0.1
				else:
					sphrase.rating = (sphrase.rating*sphrase.gamesCount+forms[i][1].cleaned_data['score'])/(sphrase.gamesCount+1)
				sphrase.gamesCount += 1
				sphrase.save()
			bestPhrase = Phrase()
			for j in range(2,players+1):
				if forms[i][j].is_valid():

					phrase = Phrase.objects.filter(name = forms[i][j].cleaned_data['phrase'])
					if not phrase:
						phrase = Phrase()
						#phrase.author = Profile.objects.get(user = User.objects.get(username = forms[i][j].cleaned_data['player']))
						phrase.name = forms[i][j].cleaned_data['phrase']
						phrase.rating = forms[i][j].cleaned_data['score']
						phrase.save()
						phraseSuccess += 1
					elif forms[i][j].cleaned_data['score'] > 0 :
						phrase = Phrase.objects.get(name = forms[i][j].cleaned_data['phrase'])
						phrase.gamesCount += 1
						if phrase.gamesCount >= 10 :
							phrase.rating = phrase.rating*0.9+forms[i][j].cleaned_data['score']*0.1
						else:
							phrase.rating = (phrase.rating*phrase.gamesCount+forms[i][j].cleaned_data['score'])/(phrase.gamesCount+1)
						phrase.save()
					phrase.author.numOfAuthoredPhrases += 1
					phrase.author.score += forms[i][j].cleaned_data['score']
					phrase.author.save()
					if phrase.rating > bestPhrase.rating:
						bestPhrase = phrase
			if bestPhrase.rating < 1:
				newPackPhrases.append(sphrase)
			else:
				newPackPhrases.append(bestPhrase)
				
		currentPack = PhrasePack.objects.get(id = packid)
		packRating /= 8
		if packRating > 3.5:
			packRating = 7 - packRating
		packRating = packRating/3.5*5
		currentPack.rating = packRating
		currentPack.gamesCount += 1
		currentPack.save()

		if phraseSuccess > 4:
			newPack = PhrasePack()
			newPack.title = "random"
			newPack.save()
			newPack.phrases.set(newPackPhrases)
			newPack.save()			
		return redirect('game-home')