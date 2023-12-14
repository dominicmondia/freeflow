from django.db import models


# Create your models here.

class Problem(models.Model):
    title = models.TextField(primary_key=True)
    id = models.IntegerField()
    problem = models.TextField()
    level = models.TextField()
    type = models.TextField()
    solution = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.title

