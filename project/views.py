from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import *
from itertools import chain


def index(request):
    game_list = Game.objects.order_by('-date_time')

    context = {
        'game_list': game_list,
    }

    return render(request, 'project/home.html', context)


# get all plays from a session
def session(request, game_id, play_id=1):
    # get the desired game
    game = get_object_or_404(Game, pk=game_id)
    # find all plays from that game
    play_detail = get_object_or_404(Play, pk=play_id)
    play_list = game.play_set

    context = {
        'game': game,
        'play_list': play_list,
        'play_id': play_id,
        'play_detail': play_detail
    }
    return render(request, 'project/session.html', context)


def play_info(request, play_id, game_id):
    # get the chosen play
    game = get_object_or_404(Game, pk=game_id)
    play = get_object_or_404(Play, pk=play_id)

    context = {
        'play': play
    }
    return render(request, 'project/play.html', context)
