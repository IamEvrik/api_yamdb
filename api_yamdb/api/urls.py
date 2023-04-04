"""URL для API."""

from rest_framework import routers

from django.urls import include, path

from api.v1 import views as v1

app_name = 'api'

v1_router = routers.SimpleRouter()
v1_router.register(r'users', v1.UserViewSet, basename='users')
v1_router.register(r'categories', v1.CategoriesViewSet, basename='categories')
v1_router.register(r'genres', v1.GenresViewSet, basename='genres')
v1_router.register(r'titles', v1.TitlesViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    v1.ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    v1.CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', v1.UserRegistrationViewSet.as_view()),
    path('v1/auth/token/', v1.UserGetToken.as_view()),
]
