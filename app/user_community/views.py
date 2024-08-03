"""Views for userCommunity APIs."""

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from user_community.models import UserCommunity
from user_community.serializers import (
    UserCommunitySerializer,
    UserCommunityFilter,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserCommunityViewSet(ModelViewSet):
    """Views for manage UserCommunity APIs."""
    serializer_class = UserCommunitySerializer
    queryset = UserCommunity.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserCommunityFilter
    pagination_class = StandardResultsSetPagination
    paginator = PageNumberPagination()

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve UserCommunity APIs."""
        return self.queryset.order_by('-id')
