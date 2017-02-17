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


class Quarterback(Player):
    pass_rating = models.IntegerField

    def __str__(self):
        return "%s %s" % (self.first_name, self.second_name)


class Play(models.Model):
    # field positions
    OWN = 'OWN'
    OPP = 'OPP'

    # possible field halves
    FIELD_HALVES = (
        (OWN, 'Own'),
        (OPP, 'Opponent\'s')
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

    class Meta:
        abstract = True

    def __str__(self):
        # e.g. (Q3 - 04:31) 3rd & 7, Pass, Gain of 14
        return "(Q%s, - %s) %s % %s, %s, Gain of %s" % (self.quarter, self.time, self.down, self.distance,
                                                        self.type, self.outcome, self.gain)


class PassPlay(Play):
    INT = 'INT',
    TD = 'TD'
    PA = 'PA'

    OUTCOMES = (
        (TD, 'Touchdown'),
        (INT, 'Interception'),
        (PA, 'Pass Attempt')

    )
    complete = models.BooleanField
    outcome = models.CharField(max_length=3, choices=OUTCOMES)
    passer = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='play_passer')
    receiver = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='play_receiver')

    def __str__(self):
        # example: Touchdown: QB #13 throws 17-Yard pass to #84
        return "#%s throws %s-Yard %s pass to %s" % (self.outcome, self.passer.jersey_no, self.gain, self.receiver)


class RunPlay(Play):
    TD = 'TD',
    FUM_REC = 'FR',
    FUM_LOST = 'FL',
    RUN = 'RN'

    OUTCOMES = (
        (TD, 'Touchdown'),
        (FUM_REC, 'Fumbled, recovered'),
        (FUM_LOST, 'Lost Fumble'),
        (RUN, 'QB Rush')
    )
    outcome = models.CharField(max_length=3, choices=OUTCOMES)
    runner = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:
        abstract = False

    def __str__(self):
        # example: Touchdown: QB #7 runs the ball for a gain of 8 yards
        return "%s: QB #%s runs the ball for a gain of %s yards" % (self.outcome, self.runner.jersey_no, self.gain)


class HandOffPlay(RunPlay):
    quarterback = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        # example: Hand-off: RB #23 runs the ball for a gain of 9 yards
        return "Hand-off: RB #%s runs the ball for a gain of %s" % (self.runner, self.gain)
