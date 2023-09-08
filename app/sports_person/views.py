"""Views for the sports_person APIs."""

from rest_framework import viewsets
# from rest_framework import filters
from django_filters import rest_framework as filters
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated

from sports_person.models import SportsPerson
from sports_person import serializers


class SportsPersonViewSet(viewsets.ModelViewSet):
    """View for manage sports_person APIs."""
    serializer_class = serializers.SportsPersonSerializer
    queryset = SportsPerson.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = serializers.SportsPersonFilter
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['last_name']

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve sports_person for auth user."""
        # return self.queryset.filter(user=self.request.user).order_by('-id')
        return self.queryset.order_by('-id')
