from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.game_homepage, name='game_homepage'),
    path('game/code/<code>', views.game_go, name='game_go'),
    path('game/code/', views.game_post, name='game_post')

    # build code url later
]
