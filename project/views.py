from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *


def index(request):
    game_list = Game.objects.order_by('date_time')

    context = {
        'game_list': game_list,
    }

    return render(request, 'project/index.html', context)
