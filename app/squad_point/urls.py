"""URL mapping for SquadPoint APIs"""

from django.urls import (path, include)

from rest_framework.routers import DefaultRouter

from squad_point.views import (
    SquadPointViewSet,
    NominationResultsView
)

app_name = 'squad_point'

router = DefaultRouter()
router.register(r'squad_point', SquadPointViewSet)
# router.register(r'result_nomination', NominationResultsView)

urlpatterns = [
    path('', include(router.urls)),
    path('result_nomination/<int:nomination_id>/', NominationResultsView.as_view(), name='result_nomination'),

]
