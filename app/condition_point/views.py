"""Views for Condition of point APIs."""

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated

from django_filters import rest_framework as filters

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.types import OpenApiTypes
# from drf_spectacular.utils import (
#     OpenApiExample,
#     expend_schema,
#     OpenApiParameter,
# )
from rest_framework.pagination import PageNumberPagination

from condition_point.models import ConditionPoint
from condition_point.serializers import (
    ConditionPointSerializer,
    ConditionPointFilter,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ConditionPointViewSet(ModelViewSet):
    """View for manage condition of point in nomination"""
    serializer_class = ConditionPointSerializer
    queryset = ConditionPoint.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ConditionPointFilter

    pagination_class = StandardResultsSetPagination

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    paginator = PageNumberPagination()

    def get_queryset(self):
        """Retrieve Condition Point API"""
        return self.queryset.order_by('-id')
    