from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=40)
    nickname = models.CharField(max_length=40)

    def __str__(self):
        return " "


class Game(models.Model):
    # define venue types
    HOME = 'H'
    AWAY = 'A'
    NEUTRAL = 'N'
    VENUE_CHOICES = (
        (HOME, 'Home'),
        (AWAY, 'Away'),
        (NEUTRAL, 'Neutral Venue')
    )
    date_time = models.DateTimeField('Game Date')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    opponent = models.CharField(max_length=50)
    venue = models.CharField(max_length=1, choices=VENUE_CHOICES)

    def __str__(self):
        return "v %s (%s)" % (self.opponent, self.venue)


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    jersey_no = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)], null=True)
    imageUrl = models.CharField(max_length=50, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.first_name, self.second_name)


class Performance(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    completions = models.IntegerField()
    attempts = models.IntegerField()
    pass_rating = models.DecimalField(max_digits=4, decimal_places=1)


class Play(models.Model):
    # field positions
    OWN = 'OWN'
    OPP = 'OPP'

    # possible field halves
    FIELD_HALVES = (
        (OWN, 'Own'),
        (OPP, 'Opponent\'s')
    )

    INT = 'INT',
    TD = 'TD',
    PA = 'PA',
    SK = 'SK'

    OUTCOMES = (
        (TD, 'Touchdown'),
        (INT, 'Interception'),
        (PA, 'Pass Attempt'),
        (SK, 'Sack')

    )

    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    # play context: down, distance, field_half, yard_line, quarter, time, outcome, gain
    down = models.IntegerField(validators=[MaxValueValidator(4), MinValueValidator(1)])
    distance = models.IntegerField(validators=[MaxValueValidator(99), MinValueValidator(0.5)])
    field_half = models.CharField(max_length=3, choices=FIELD_HALVES)
    yard_line = models.IntegerField(validators=[MaxValueValidator(50), MinValueValidator(0.5)])
    quarter = models.IntegerField(validators=[MaxValueValidator(4), MinValueValidator(1)])
    time = models.TimeField()  # need to somehow make sure this displays as MM:SS
    gain = models.IntegerField(validators=[MaxValueValidator(100)])

    complete = models.BooleanField(default=False)
    outcome = models.CharField(max_length=3, choices=OUTCOMES)
    passer = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='play_passer')
    receiver = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='play_receiver')

    vid_url = models.CharField(max_length=50, null=True)
    vid_url_alt = models.CharField(max_length=50, null=True)
    vid_url_alt2 = models.CharField(max_length=50, null=True)

    air_yards = models.IntegerField(validators=[MaxValueValidator(100)], null=True)
    accurate = models.BooleanField(default=True)

    note = models.TextField(max_length=300, null=True)

    def __str__(self):
        # e.g. (Q3 - 04:31) 3rd & 7, Gain of 14
        return "(Q%s, - %s) %s & %s %s, Gain of %s" % (self.quarter, self.time, self.down, self.distance, self.outcome,
                                                     self.gain)
