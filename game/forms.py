from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RoundResultFull(forms.Form):
	player = forms.CharField()
	phrase = forms.CharField()
	score = forms.IntegerField()

class RoundResultScoreOnly(forms.Form):
	score = forms.IntegerField()

class LoginForm(forms.Form):
	name = forms.CharField()

class ChooseAnswer(forms.Form):
	Your_Choice = forms.TypedChoiceField(choices=[(x, x) for x in range(1, 9)], coerce=int)
	#Your_Choice = forms.IntegerField()