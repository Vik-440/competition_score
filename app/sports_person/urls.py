"""URL mapping for the sports_person app"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from sports_person import views


sports_person_router = DefaultRouter()
sports_person_router.register('sports_person', views.SportsPersonViewSet)
city_router = DefaultRouter()
city_router.register('city', views.CityViewSet)
team_router = DefaultRouter()
team_router.register('team', views.TeamViewSet)
rank_router = DefaultRouter()
rank_router.register('rank', views.RankViewSet)

urlpatterns = [
    path('', include(sports_person_router.urls)),
    path('', include(city_router.urls)),
    path('', include(team_router.urls)),
    path('', include(rank_router.urls)),
]
