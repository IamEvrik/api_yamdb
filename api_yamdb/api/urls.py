"""URL для API."""

from rest_framework import routers

from django.urls import include, path

from api.views import (CategoriesViewSet, GenresViewSet, ReviewViewSet, TitlesViewSet,
                       UserGetToken, UserRegistrationViewSet, UserViewSet)

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
    
urlpatterns = [
    path('', include(router.urls), name='users'),
    path('auth/signup/', UserRegistrationViewSet.as_view()),
    path('auth/token/', UserGetToken.as_view()),
]
