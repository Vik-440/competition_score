"""URL mapping for Squad APIs"""

from django.urls import (path, include)

from rest_framework.routers import DefaultRouter

from squad.views import SquadViewSet

app_name = 'squad'

router = DefaultRouter()
router.register(r'squad', SquadViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
