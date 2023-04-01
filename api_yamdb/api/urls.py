from django.urls import path, include
from rest_framework import routers

from .views import CategoriesViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'categories', CategoriesViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]