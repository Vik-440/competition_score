"""URL mapping for SquadPoint APIs"""

from django.urls import (path, include)

from rest_framework.routers import DefaultRouter

from squad_point.views import SquadPersonViewSet

app_name = 'squad_point'

router = DefaultRouter()
router.register(r'squad_point', SquadPersonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
