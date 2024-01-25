"""Views for QSquadPoint APIs"""

from rest_framework.viewsets import (
    ModelViewSet,
)
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination

from squad_point.models import SquadPoint
from squad_point.serializers import(
    SquadPointSerializer,
    SquadPointFilter,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class SquadPersonViewSet(ModelViewSet):
    """View for manage SquadPoint APIs."""
    serializer_class = SquadPointSerializer
    queryset = SquadPoint.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = SquadPointFilter

    pagination_class = PageNumberPagination

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    paginator = PageNumberPagination()

    def get_queryset(self):
        """Retrieve SquadPoint API"""
        return self.queryset.order_by('-id')