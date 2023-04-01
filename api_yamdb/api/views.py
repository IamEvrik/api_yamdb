from rest_framework import viewsets, filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from reviews.models import Categories
from .permissions import IsAdminOrReadOnly
from .serializers import CategoriesSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]

    def destroy(self, request, *args, **kwargs):
        slug = self.kwargs['pk']
        category = get_object_or_404(Categories, slug=slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


