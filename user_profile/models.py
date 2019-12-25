from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
# Create your models here.
class Profile(models.Model):
	status = models.CharField(default="user",max_length=100)
	score = models.IntegerField(default=0)
	numOfAuthoredPhrases = models.IntegerField(default=0)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100,default="unnamed")
	number = models.CharField(max_length=12,null=True)
	rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
	isReady = models.BooleanField(default=False)
	def __str__(self):
		return self.name
	