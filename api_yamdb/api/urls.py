from django.urls import path, include
from rest_framework import routers

from .views import CategoriesViewSet, GenresViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'genres', GenresViewSet, basename='genres')

urlpatterns = [
    path('v1/', include(router.urls)),
]