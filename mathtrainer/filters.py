import django_filters
from django.db.models import Q
from .models import Problem


class ProblemFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="content_filter", label='')
    level = django_filters.ChoiceFilter(choices=Problem.LevelChoices.choices, label='',)

    class Meta:
        model = Problem
        fields = ['level', 'q']

    def content_filter(self, queryset, name,  value):
        return queryset.filter(
            Q(problem__icontains=value) |
            Q(title__icontains=value)
        )
