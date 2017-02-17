from django.db import models


class Game(models.Model):
    date_time = models.DateTimeField('Game Date')
    opponent = models.CharField(max_length=50)

    def __str__(self):
        return self.date_time


class Player(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Play(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    qb = models.ForeignKey(Player, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


