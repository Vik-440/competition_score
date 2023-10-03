"""Views for Nomination and Conditions APIs."""

from rest_framework.viewsets import (
    ModelViewSet,
    # status,
)
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from django_filters import rest_framework as filters
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from drf_spectacular.types import OpenApiTypes
# from drf_spectacular.utils import (
#     extend_schema,
#     OpenApiExample,
#     OpenApiParameter,
# )
from rest_framework.pagination import PageNumberPagination

from nomination.models import (
    Nomination,
    ConditionPerformance,
)
from nomination.serializers import (
    NominationSerializer,
    ConditionPerformanceSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class NominationViewSet(ModelViewSet):
    """View for manage Nomination APIs"""
    # queryset = Nomination.objects.select_related('competition').all()
    serializer_class = NominationSerializer
    queryset = Nomination.objects.all()
    # filter_backends = [filters.DjangoFilterBackend]
    # filterset_class = serializers.SportsPersonFilter

    pagination_class = StandardResultsSetPagination

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    paginator = PageNumberPagination()

    def get_queryset(self):
        """Retrieve Nomination API"""
        return self.queryset.order_by('-id')


class ConditionPerformanceViewSet(ModelViewSet):
    """View for manage Conditions of performance API"""
    serializer_class = ConditionPerformanceSerializer
    queryset = ConditionPerformance.objects.all()
    # filter_backends = [filters.DjangoFilterBackend]
    # filterset_class = serializers.SportsPersonFilter

    pagination_class = StandardResultsSetPagination

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    paginator = PageNumberPagination()

    def get_queryset(self):
        """Retrieve Conditions of performance API"""
        return self.queryset.order_by('-id')
