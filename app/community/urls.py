"""URL mapping for the community app"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from community.views import CommunityViewSet

app_name = 'community'
router = DefaultRouter()
router.register(r'community', CommunityViewSet)

urlpatterns = [path('', include(router.urls)), ]