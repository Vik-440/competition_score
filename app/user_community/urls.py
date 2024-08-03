"""URL mapping for UserCommunity APIs."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user_community.views import UserCommunityViewSet

app_name = 'user_community'
router = DefaultRouter()
router.register(r'user_community', UserCommunityViewSet)

urlpatterns = [path('', include(router.urls)),]
