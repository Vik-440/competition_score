"""URL mapping for Nomination and Conditions APIs"""

from django.urls import (path, include)

from rest_framework.routers import DefaultRouter

from nomination.views import (
    NominationViewSet,
    ConditionPerformanceViewSet,
)

app_name = 'nomination'

# router1 = DefaultRouter()
# router2 = DefaultRouter()
# router1.register('', NominationViewSet)
# router2.register('cond_perform', ConditionPerformanceViewSet)

# urlpatterns = [
#     path('', include(router1.urls)),
#     path(r'cond_perform/', include(router2.urls)),
# ]

router = DefaultRouter()
router.register(r'nomination', NominationViewSet)
router.register(r'condition_perform', ConditionPerformanceViewSet)

# urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls)),
]
