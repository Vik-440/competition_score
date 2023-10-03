"""URL mapping for the sports_person app"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from sports_person.views import (
    SportsPersonViewSet,
    PersonRankViewSet,
)

app_name = 'sports_person'

# router1 = DefaultRouter()
# router1.register('', views.SportsPersonViewSet)
# router2 = DefaultRouter()
# router2.register('rank', views.PersonRankViewSet)

# urlpatterns = [
#     path('', include(router1.urls)),
#     path(r'rank/', include(router2.urls)),
# ]

router = DefaultRouter()
router.register(r'sports_person', SportsPersonViewSet)
router.register(r'person_rank', PersonRankViewSet)

# urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls)),
]
