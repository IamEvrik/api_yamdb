"""Кастомные фильтры."""

import django_filters.rest_framework as dfilters

from reviews.models import Titles


class CharFilterInFilter(dfilters.BaseInFilter, dfilters.CharFilter):
    """Базовый класс для фильтрации по текстовому полю."""


class TitleFilter(dfilters.FilterSet):
    """Настройка фильтрации произведений."""

    genre = CharFilterInFilter(field_name='genre__slug', lookup_expr='in')
    category = CharFilterInFilter(field_name='category__slug',
                                  lookup_expr='in')

    class Meta:
        model = Titles
        fields = ['genre', 'category', 'name', 'year']
