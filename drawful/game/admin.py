from django.contrib import admin
from .models import Phrase, PhrasePack, PlayedGame, OnlineGame, Image, Round



# Register your models here.
admin.site.register(Phrase)

admin.site.register(PhrasePack)

admin.site.register(PlayedGame)

admin.site.register(OnlineGame)

admin.site.register(Round)

admin.site.register(Image)