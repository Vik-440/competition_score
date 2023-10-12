"""URL mapping for the sports_person app"""

from django.urls import (path, include)

from rest_framework.routers import DefaultRouter

from sports_person.views import (
    SportsPersonViewSet,
    PersonRankViewSet,
)

app_name = 'sports_person'

router = DefaultRouter()
router.register(r'sports_person', SportsPersonViewSet)
router.register(r'person_rank', PersonRankViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
