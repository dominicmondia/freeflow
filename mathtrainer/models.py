from django.db import models
from django.contrib.auth.models import User


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
    level = models.TextField(choices=LevelChoices.choices)
    type = models.TextField()
    solution = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    history = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.user.username


class ProblemReport(models.Model):

    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.problem_id.title


class Flow(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET("anonymous"))
    title = models.CharField(max_length=150, primary_key=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class FlowSection(models.Model):
    problems = models.JSONField(default=list, blank=True)
    title = models.CharField(max_length=150)
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
