from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import *
from itertools import chain
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm


def index(request):
    game_list = Game.objects.order_by('-date_time')

    context = {
        'game_list': game_list,
    }

    return render(request, 'project/home.html', context)


# get all plays from a session
def session(request, game_id, play_id=1, team_id=1):
    game_list = Game.objects.order_by('-date_time')
    # get the desired game
    game = get_object_or_404(Game, pk=game_id)
    # find all plays from that game
    first_play = game.play_set.first()
    # workaround to load the correct play by default
    if play_id == 1:
        play_detail = get_object_or_404(Play, pk=first_play.id)
    else:
        play_detail = get_object_or_404(Play, pk=play_id)
    play_list = Play.objects.filter(game=game_id)
    other_games = Game.objects.exclude(pk=game_id).filter(team=team_id)
    all_plays = Play.objects.all()
    w, h = game_list.count()+1, 4
    prev_game_plays = [[Play() for x in range(w)] for y in range(h)]
    quarter_yardage_totals = [[0 for x in range(w)] for y in range(h)]
    prev_game_comp = [[0 for x in range(w)] for y in range(h)]
    prev_game_att = [[0 for x in range(w)] for y in range(h)]

    r = play_detail.receiver
    receiver_performance = [0, 0, 0, 0]  # targets, catches, yards, touchdowns
    routes = []
    passer_routes = []
    passer_routes_comp = []
    pass_receivers = []
    best_receivers = []

    for p in play_list:
        if p.receiver == r:
            receiver_performance[0] += 1  # add 1 to targets
            if p.complete:
                receiver_performance[1] += 1  # add 1 to catches
                receiver_performance[2] += p.gain  # add gain to yards
                routes.append(p.route)
                if p.outcome == 'TD':
                    receiver_performance[3] += 1

    for p in play_list:
        passer_routes.append(p.route)
        pass_receivers.append(p.receiver)
        if p.complete:
            passer_routes_comp.append(p.route)
            best_receivers.append(p.receiver)

        fav = "N/A"
        qb_fav = "N/A"
        qb_fav_comp = "N/A"
        qb_fav_receiver = "N/A"
        best_receiver = "N/A"
        try:
            fav = max(set(routes), key=routes.count)
            qb_fav = max(set(passer_routes), key=passer_routes.count)
            qb_fav_comp = max(set(passer_routes_comp), key=passer_routes_comp.count)
            qb_fav_receiver = max(set(pass_receivers), key=pass_receivers.count)
            best_receiver = max(set(best_receivers), key=best_receivers.count)
        except ValueError:
            pass


    for z in range(game_list.count()):
        for i in range(4):
            prev_game_plays[z][i] = list(Play.objects.filter(game=str(z + 1), quarter=i+1).values_list('id', flat=True))
            quarter_yardage_totals[z][i] = sum(Play.objects.filter(game=str(z + 1), quarter=i+1).values_list('gain', flat=True))
            prev_game_comp[z][i] = sum(Play.objects.filter(game=str(z + 1), quarter=i+1, complete=True).values_list('complete', flat=True))
            prev_game_att[z][i] = sum((Play.objects.filter(game=str(z + 1), quarter=i+1).exclude(outcome="SK").values_list('passer', flat=True)))

    season_avg_comp = [0, 0, 0, 0]
    season_total_att = [0, 0, 0, 0]
    season_avg_pct = [0, 0, 0, 0]
    season_total_comp = [0, 0, 0, 0]
    season_avg_att = [0, 0, 0, 0]
    season_ypa = [0, 0, 0, 0]

    for g in range(game_list.count()):
        season_avg_comp[0] += prev_game_comp[g][0]
        season_avg_comp[1] += prev_game_comp[g][1]
        season_avg_comp[2] += prev_game_comp[g][2]
        season_avg_comp[3] += prev_game_comp[g][3]
        season_total_att[0] += prev_game_att[g][0]
        season_total_att[1] += prev_game_att[g][1]
        season_total_att[2] += prev_game_att[g][2]
        season_total_att[3] += prev_game_att[g][3]
        season_total_comp[0] += prev_game_comp[g][0]
        season_total_comp[1] += prev_game_comp[g][1]
        season_total_comp[2] += prev_game_comp[g][2]
        season_total_comp[3] += prev_game_comp[g][3]
        if season_avg_att[0] != 0:
            season_ypa[0] += (quarter_yardage_totals[g][0] / (season_total_att[0]/game_list.count()))
        if season_avg_att[1] != 0:
            season_ypa[1] += (quarter_yardage_totals[g][1] / (season_total_att[1]/game_list.count()))
        if season_avg_att[2] != 0:
            season_ypa[2] += (quarter_yardage_totals[g][2] / season_avg_att[2])
        if season_avg_att[3] != 0:
            season_ypa[3] += (quarter_yardage_totals[g][3] / season_avg_att[3])


    prev_game_pct = [[0 for x in range(w)] for y in range(h)]
    for g in range(game_list.count()):
        for i in range(4):
            if prev_game_att[g][i] != 0:
                prev_game_pct[g][i] = round(((prev_game_comp[g][i] / prev_game_att[g][i]) * 100), 1)
                season_avg_pct[i] = round(((season_total_comp[i] / season_total_att[i]) * 100), 1)


    for a in range(4):
        season_avg_comp[a] = round((season_avg_comp[a] / game_list.count()), 1)

    # for each element of team_game
    # find all plays in play_list that share the game ID
    # store the gains of these plays in an array
    # gains = [[[] for i in range(4)] for i in range(4)]
    # other_plays = [[] for i in range(other_games.count())]

    q1yards = 0
    q2yards = 0
    q3yards = 0
    q4yards = 0

    for a in all_plays:
        if a.quarter == 1:
            q1yards += a.gain
        if a.quarter == 2:
            q2yards += a.gain
        if a.quarter == 3:
            q3yards += a.gain
        if a.quarter == 4:
            q4yards += a.gain

    avg_q1yards = round((q1yards / game_list.count()), 0)
    avg_q2yards = round(q2yards / game_list.count(), 0)
    avg_q3yards = round(q3yards / game_list.count(), 0)
    avg_q4yards = round(q4yards / game_list.count(), 0)

    season_ypa[0] = round((avg_q1yards / season_total_att[0]), 1)

    avg_yards_cum = [0, 0, 0, 0]

    avg_yards_cum[0] = avg_q1yards
    avg_yards_cum[1] = avg_yards_cum[0] + avg_q2yards
    avg_yards_cum[2] = avg_yards_cum[1] + avg_q3yards
    avg_yards_cum[3] = avg_yards_cum[2] + avg_q4yards



    play_tagline = "%s-yard %s at %s %s (Q%s %s)" % (play_detail.gain, play_detail.outcome, play_detail.field_half,
                                                     play_detail.yard_line, play_detail.quarter, play_detail.time)

    w = 0
    h = 5
    for g in game_list:
        w += 1
    matrix = [[0 for x in range(w)] for y in range(h)]


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

    avg_comp_statement = " "
    avg_yards_statement = " "
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
        if q_plays[q] > 0:
            q_pct[q] = round(((totalcomp[q] / q_plays[q]) * 100), 1)

    q_yards_cum[0] = q_yards[0]
    q_yards_cum[1] = q_yards_cum[0] + q_yards[1]
    q_yards_cum[2] = q_yards_cum[1] + q_yards[2]
    q_yards_cum[3] = q_yards_cum[2] + q_yards[3]

    q_ypa = [0, 0, 0, 0]
    for q in range(len(q_ypa)):
        if q_plays[q] > 0:
            q_ypa[q] = round(q_yards[q] / q_plays[q], 1)

    pct_diff = avg_comp - pct

    yac = play_detail.gain - play_detail.air_yards
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
        'q_ypa': q_ypa,
        'game_list': game_list,
        'other_games': other_games,
        'q1yards': q1yards,
        'q2yards': q2yards,
        'q3yards': q3yards,
        'q4yards': q4yards,
        'avg_q1yards': avg_q1yards,
        'avg_q2yards': avg_q2yards,
        'avg_q3yards': avg_q3yards,
        'avg_q4yards': avg_q4yards,
        'avg_yards_cum': avg_yards_cum,
        'pct_diff': pct_diff,
        'yac': yac,
        'prev_game_plays': prev_game_plays,
        'quarter_yardage_totals': quarter_yardage_totals,
        'receiver_performance': receiver_performance,
        'routes': routes,
        'fav': fav,
        'prev_game_comp': prev_game_comp,
        'prev_game_att': prev_game_att,
        'season_avg_comp': season_avg_comp,
        'season_total_att': season_total_att,
        'prev_game_pct': prev_game_pct,
        'season_avg_pct': season_avg_pct,
        'qb_fav': qb_fav,
        'qb_fav_comp': qb_fav_comp,
        'qb_fav_receiver': qb_fav_receiver,
        'best_receiver': best_receiver,
        'season_ypa': season_ypa
    }
    return render(request, 'project/session.html', context)


def about(request):

    return render(request, 'project/about.html')


class NoteForm(ModelForm):
    class Meta:
        model = Play
        fields = ['note']

