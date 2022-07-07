from django.urls import path, include
from rest_framework import routers

from .views import (ArticleViewSet, CommentViewSet, DepartmentCodeViewSet,
                    ProfileViewSet, MyProfileListView, BelongsViewSet)

router = routers.DefaultRouter()
router.register('article',ArticleViewSet)
router.register('comment',CommentViewSet)
router.register('profile',ProfileViewSet)
router.register('department',DepartmentCodeViewSet)
router.register('belongs', BelongsViewSet)
app_name = 'apiv1'

urlpatterns = [
    path('me/', MyProfileListView.as_view(), name='myprofile'),
    path('', include(router.urls))
]