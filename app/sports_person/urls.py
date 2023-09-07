"""URL mapping for the sports_person app"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from sports_person import views


# sports_person_router = DefaultRouter()
# sports_person_router.register('sports_person', views.SportsPersonViewSet)
# city_router = DefaultRouter()
# city_router.register('city', views.CityViewSet)
# team_router = DefaultRouter()
# team_router.register('team', views.TeamViewSet)
# rank_router = DefaultRouter()
# rank_router.register('rank', views.RankViewSet)

router = DefaultRouter()
router.register(r'person', views.SportsPersonViewSet)
router.register(r'city', views.CityViewSet)
router.register(r'team', views.TeamViewSet)
router.register(r'rank', views.RankViewSet)

app_name = 'sports_person'

# urlpatterns = [
#     path('person/', include(sports_person_router.urls)),
#     path('city/', include(city_router.urls)),
#     path('team/', include(team_router.urls)),
#     path('rank/', include(rank_router.urls)),
# ]
urlpatterns = [
    path('', include(router.urls)),
    # path('city/', views.CityViewSet, name='city'),
    # path('team/', views.TeamViewSet, name='team'),
    # path('rank/', views.RankViewSet, name='rank'),
]
