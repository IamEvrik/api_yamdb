from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Categories, Genres
from .permissions import IsAdminOrReadOnly
from .serializers import CategoriesSerializer, GenresSerializer


class CustomizeViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):

    """Кастомизированный вьюсет только на просмотр, создание и удаление"""

    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class CategoriesViewSet(CustomizeViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(CustomizeViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
