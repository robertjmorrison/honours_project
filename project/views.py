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
    # play_list = game.play_set
    play_list = Play.objects.filter(game=game_id)

    play_tagline = "%s-yard %s at %s %s (Q%s %s)" % (play_detail.gain, play_detail.outcome, play_detail.field_half,
                                                     play_detail.yard_line, play_detail.quarter, play_detail.time)

    test = " "
    comp_count = 0
    total_plays = 0
    td = 0
    interceptions = 0
    yards = 0
    pct = 0
    avg_comp = 61
    avg_yards = 257
    ncaa_formula = 0
    ncaa_rating = 0

    for p in play_list:
        if p.outcome != 'SK':
            total_plays += 1
            yards = yards + p.gain
        if p.complete:
            comp_count += 1
        if p.outcome == 'TD':
            td += 1
        if p.outcome == 'INT':
            interceptions += 1

    # calculations - if statement used to prevent division by zero
    if total_plays > 0:
        pct = round((comp_count/total_plays * 100), 1)
        ncaa_formula = ((8.4 * yards) + (330 * td) + (100 * comp_count) - (200 * interceptions)) / total_plays
        ncaa_rating = round(ncaa_formula, 1)

    avg_comp_statement = ""
    avg_yards_statement = ""
    if avg_comp > pct:
        avg_comp_statement = "Below Average"
    else:
        avg_comp_statement = "Above Average"

    if avg_yards > yards:
        avg_yards_statement = "Below Average"
    else:
        avg_yards_statement = "Above Average"

    q_yards = [0, 0, 0, 0]
    q_yards_cum = [0, 0, 0, 0]

    totalcomp = [0, 0, 0, 0]
    q_plays = [0, 0, 0, 0]
    q_pct = [0, 0, 0, 0]

    for p in play_list:
        if p.quarter == 1:
            q_yards[0] = q_yards[0] + p.gain
            q_plays[0] += 1
            if p.complete:
                totalcomp[0] += 1
        if p.quarter == 2:
            q_yards[1] = q_yards[1] + p.gain
            q_plays[1] += 1
            if p.complete:
                totalcomp[1] += 1
        if p.quarter == 3:
            q_yards[2] = q_yards[2] + p.gain
            q_plays[2] += 1
            if p.complete:
                totalcomp[2] += 1
        if p.quarter == 4:
            q_yards[3] = q_yards[3] + p.gain
            q_plays[3] += 1
            if p.complete:
                totalcomp[3] += 1

    for q in range(len(q_pct)):
        q_pct[q] = round(((totalcomp[q] / q_plays[q]) * 100), 1)

    q_yards_cum[0] = q_yards[0]
    q_yards_cum[1] = q_yards_cum[0] + q_yards[1]
    q_yards_cum[2] = q_yards_cum[1] + q_yards[2]
    q_yards_cum[3] = q_yards_cum[2] + q_yards[3]

    q_ypa = [0, 0, 0, 0]
    for q in range(len(q_ypa)):
        q_ypa[q] = round(q_yards[q] / q_plays[q], 1)

    context = {
        'game': game,
        'play_list': play_list,
        'play_id': play_id,
        'play_detail': play_detail,
        'play_tagline': play_tagline,
        'test': test,
        'comp_count': comp_count,
        'total_plays': total_plays,
        'td': td,
        'interceptions': interceptions,
        'yards': yards,
        'ncaa_rating': ncaa_rating,
        'pct': pct,
        'avg_comp_statement': avg_comp_statement,
        'avg_yards_statement': avg_yards_statement,
        'q_yards': q_yards,
        'totalcomp': totalcomp,
        'q_pct': q_pct,
        'q_plays': q_plays,
        'q_yards_cum': q_yards_cum,
        'q_ypa': q_ypa
    }
    return render(request, 'project/session.html', context)


def about(request):

    return render(request, 'project/about.html')
