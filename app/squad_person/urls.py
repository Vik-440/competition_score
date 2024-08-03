"""URL mapping for SquadPerson APIs"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from squad_person.views import SquadPersonViewSet

app_name = 'squad_person'

router = DefaultRouter()
router.register(r'squad_person', SquadPersonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
