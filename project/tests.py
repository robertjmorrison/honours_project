from django.test import TestCase
from project.models import *

# Create your tests here.


class GameTestCase(TestCase):

    def test_game_instantiates_correctly(self):
        """tests that game objects are correctly set up
        by comparing the expected output of each field to
        the actual output"""
        team = Team.objects.create()
        game = Game.objects.create(date_time='2016-01-01 15:00', team=team, opponent="Glasgow Tigers", venue="A", result="L",
                            points_for=13, points_against=37)

        self.assertEqual(game.date_time, '2016-01-01 15:00')
        self.assertEqual(game.team, team)
        self.assertEqual(game.opponent, "Glasgow Tigers")
        self.assertEqual(game.venue, 'A')
        self.assertEqual(game.result, 'L')
        self.assertEqual(game.points_for, 13)
        self.assertEqual(game.points_against, 37)


