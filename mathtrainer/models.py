from django.db import models


# Create your models here.

class ProblemType(models.Model):
    type = models.TextField(primary_key=True)

    def __str__(self):
        return self.type


class Problem(models.Model):
    title = models.TextField(primary_key=True)
    id = models.IntegerField()
    problem = models.TextField()
    level = models.TextField()
    type = models.ForeignKey(ProblemType, on_delete=models.CASCADE)
    solution = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.title

