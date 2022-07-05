from django.urls import path, include
from rest_framework import routers

from .views import ArticleViewSet

router = routers.DefaultRouter()
router.register('article',ArticleViewSet)
app_name = 'apiv1'

urlpatterns = [
    path('', include(router.urls))
]