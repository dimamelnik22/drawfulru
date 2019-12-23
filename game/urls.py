from django.conf.urls import url
from . import views
from django.urls import path, include

urlpatterns = [
	path('', views.home_view, name="game-home"),	
	path('auth/', views.auth_view, name="game-auth"),	
	path('nick/', views.nick_view, name="game-nick"),
	path('number/', views.number_view, name="game-number"),	
	path('room/<packid>/', views.room_view, name="game-room"),
	path('room/<gameid>/join', views.roomjoin_view, name="game-roomjoin"),
	path('room/<gameid>/draw/', views.lobby_view, name="game-lobby"),
	path('room/<gameid>/wait/<roundid>/<nextstage>', views.wait_view, name="game-wait"),
	path('room/<gameid>/suggest/<roundid>', views.suggesting_view, name="game-suggesting"),
	path('room/<gameid>/guess/<roundid>', views.guessing_view, name="game-guessing"),
	path('room/<gameid>/result/<roundid>', views.result_view, name="game-result"),
	path('room/<gameid>/end', views.end_view, name="game-end"),
	path('login', views.login_view, name="game-login"),

	path('accounts/', include('allauth.urls'))
]