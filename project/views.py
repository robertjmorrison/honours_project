from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *


def index(request):
    game_list = Game.objects.order_by('-date_time')

    context = {
        'game_list': game_list,
    }

    return render(request, 'project/home.html', context)


# get all plays from a session
def session(request):
    play_list = Game.Play.objects.order_by('play')

    context = {
        'play_list': play_list,
    }
    return render(request, 'project/session.html', context)
