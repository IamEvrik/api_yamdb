from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from reviews.models import Review, Title, User
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    '''Пишу вьюсет для отзывов и рейтингов'''
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()
