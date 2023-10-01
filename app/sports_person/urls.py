"""URL mapping for the sports_person app"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from sports_person import views


router1 = DefaultRouter()
router1.register('', views.SportsPersonViewSet)
router2 = DefaultRouter()
router2.register('rank', views.PersonRankViewSet)

app_name = 'sports_person'

urlpatterns = [
    path('', include(router1.urls)),
    path('rank/', include(router2.urls)),
]
