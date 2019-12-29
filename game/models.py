from django.db import models
import datetime
from user_profile.models import Profile
import random


class Phrase(models.Model):

	name = models.CharField(max_length=100)
	author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
	gamesCount = models.IntegerField(default=0)
	rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
	def __str__(self):
		return self.name

class PhrasePack(models.Model):
	title = models.CharField(max_length=100)
	phrases = models.ManyToManyField(Phrase)
	rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
	gamesCount = models.IntegerField(default=0)
	def __str__(self):
		return self.title
	def randomPack(self):
		count = PhrasePack.objects.all().count()
		random_index = randint(0, count - 1)
		return random.sample(Phrase.objects.all(), numOfObjects)

class PlayedGame(models.Model):
	playDate = models.DateField(("Date"), default=datetime.date.today)
	players = models.ManyToManyField(Profile)
	phrasePack = models.ForeignKey(PhrasePack, on_delete=models.SET_NULL, null=True)
	def __str__(self):
		return str(self.playDate)

class Image(models.Model):

    image = models.TextField()
    canvas_image = models.TextField()

class Round(models.Model):
	image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
	player = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
	finished = models.BooleanField(default=False)	
	phrases = models.ManyToManyField(Phrase)

class PlayersChoice(models.Model):
	player = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
	chosenPhrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)
	ground = models.ForeignKey(Round, on_delete=models.CASCADE)

class PlayersNewPhrase(models.Model):
	player = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
	newPhrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)
	ground = models.ForeignKey(Round, on_delete=models.CASCADE)

class OnlineGame(models.Model):
	players = models.ManyToManyField(Profile)
	phrasePack = models.ForeignKey(PhrasePack, on_delete=models.SET_NULL, null=True)
	isStarted = models.BooleanField(default=False)
	rounds = models.ManyToManyField(Round)
	curround = models.IntegerField(default = 0)
	playersready = models.BooleanField(default = False)




