"""Views for SquadPerson APIs."""

from rest_framework.viewsets import (
    ModelViewSet,
)
from rest_framework.pagination import PageNumberPagination

from squad_person.models import SquadPerson
from squad_person.serializers import SquadPersonSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class SquadPersonViewSet(ModelViewSet):
    """View for manage Squad APIs."""
    serializer_class = SquadPersonSerializer
    queryset = SquadPerson.objects.all()
    # filter_backends = [filters.DjangoFilterBackend]
    # filterset_class = serializers.SportsPersonFilter

    pagination_class = StandardResultsSetPagination

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    paginator = PageNumberPagination()

    def get_queryset(self):
        """Retrieve Squad API"""
        return self.queryset.order_by('-id')
