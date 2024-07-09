"""URL mapping for Condition points API."""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from condition_point.views import ConditionPointViewSet

app_name = 'condition_point'

router = DefaultRouter()
router.register(r'condition_point', ConditionPointViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
