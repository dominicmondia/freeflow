from django.contrib import admin
from .models import Problem, ProblemType

# Register your models here.
admin.site.register(Problem)
admin.site.register(ProblemType)
