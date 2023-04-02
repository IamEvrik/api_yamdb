import django_filters.rest_framework as dfilters

from reviews.models import User, Categories, Genres, Titles


class CharFilterInFilter(dfilters.BaseInFilter, dfilters.CharFilter):
    pass


class TitleFilter(dfilters.FilterSet):
    genre = CharFilterInFilter(field_name='genre__slug', lookup_expr='in')
    category = CharFilterInFilter(field_name='category__slug',
                                  lookup_expr='in')

    class Meta:
        model = Titles
        fields = ['genre', 'category', 'name', 'year']
