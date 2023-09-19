"""URL mapping for the Competition APP."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from competition.views import CompetitionViewSet

router = DefaultRouter()
router.register('', CompetitionViewSet)

app_name = 'competition'

urlpatterns = [
    path('', include(router.urls))
]
