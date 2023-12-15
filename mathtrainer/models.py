from django.db import models


class Problem(models.Model):
    class LevelChoices(models.TextChoices):
        Level_1 = 'Level 1'
        Level_2 = 'Level 2'
        Level_3 = 'Level 3'
        Level_4 = 'Level 4'
        Level_5 = 'Level 5'

    title = models.TextField(primary_key=True)
    id = models.IntegerField()
    problem = models.TextField()
    level = models.TextField()
    type = models.TextField(choices=LevelChoices.choices)
    solution = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.title

