"""Views for Community groups APIs."""

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from community.serializers import (
    CommunitySerializer,
    CommunityFilter,)
from community.models import Community


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommunityViewSet(ModelViewSet):
    """Views for manage Community APIs."""
    serializer_class = CommunitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommunityFilter
    pagination_class = StandardResultsSetPagination
    paginator = PageNumberPagination()
    queryset = Community.objects.all()
    # lookup_field = 'name'

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve Community groups"""
        return self.queryset.order_by('-id')
