"""URL mapping for the sports_person app"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from sports_person import views


router = DefaultRouter()
router.register('', views.SportsPersonViewSet)

app_name = 'sports_person'

urlpatterns = [
    path('', include(router.urls)),
]
