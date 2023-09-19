""""Views for the Competition APIs."""

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from competition.models import Competition
from competition.serializers import (
    CompetitionSerializer,
    CompetitionFilter,
)


class StandardResultSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100


class CompetitionViewSet(viewsets.ModelViewSet):
    """View for Competition APIs."""
    serializer_class = CompetitionSerializer
    queryset = Competition.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompetitionFilter
    pagination_class = StandardResultSetPagination

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    paginator = PageNumberPagination()

    def get_queryset(self):
        # return self.queryset.order_by('-competition_date').reverse()
        return self.queryset.order_by('-id')
