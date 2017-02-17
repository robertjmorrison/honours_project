from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
    opponent = models.CharField(max_length=50)
    venue = models.CharField(max_length=1, choices=VENUE_CHOICES)

    def __str__(self):
        return "v %s (%s)" % (self.opponent, self.venue)


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    jersey_no = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)]).unique

    def __str__(self):
        return "%s %s" % (self.first_name, self.second_name)


class Play(models.Model):
    # define play types here in human-readable constant
    PASS = 'PA'
    QB_RUN = 'QR'
    HAND_OFF = 'HO'

    PLAY_TYPES = (
        (PASS, 'Pass'),
        (QB_RUN, 'Quarterback Run'),
        (HAND_OFF, 'Hand-Off')
    )

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    qb = models.ForeignKey(Player, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=PLAY_TYPES)

    # play context: down, distance, field_half, yard_line, quarter, time, timeouts

    down = models.IntegerField(validators=[MaxValueValidator(4), MinValueValidator(1)])
    distance = models.IntegerField(validators=[MaxValueValidator(99), MinValueValidator(0.5)])
    OWN = 'OWN'
    OPP = 'OPP'

    FIELD_HALVES = (
        (OWN, 'Own'),
        (OPP, 'Opponent\'s')
    )

    def __str__(self):
        # e.g. (Q3 - 04:31) 3rd & 7, Pass, Gain of 14
        return "(Q%s, - %s) %s % %s, %s, Gain of %s" % (self.quarter, self.time, self.down, self.distance,
                                                        self.type, self.outcome)
