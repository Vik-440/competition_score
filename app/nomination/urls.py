"""URL mapping for Nomination and Conditions APIs"""

from django.urls import (path, include)

from rest_framework.routers import DefaultRouter

from nomination.views import (
    NominationViewSet,
    ConditionPerformanceViewSet,
)

app_name = 'nomination'

router = DefaultRouter()
router.register(r'nomination', NominationViewSet)
router.register(r'condition_performance', ConditionPerformanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
