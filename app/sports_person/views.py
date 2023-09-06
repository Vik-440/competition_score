"""Views for the sports_person APIs."""

from rest_framework import viewsets
# from rest_framework import filters
from django_filters import rest_framework as filters
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated

from sports_person.models import (
    SportsPerson,
    RankSportsPerson,
    City,
    Team,
)
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


class CityViewSet(viewsets.ModelViewSet):
    """View for manage city APIs."""
    serializer_class = serializers.CitySerializer
    queryset = City.objects.all()
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve city for auth user."""
        return self.queryset.order_by('-id')


class RankViewSet(viewsets.ModelViewSet):
    """View for manage rank APIs."""
    serializer_class = serializers.RankSerializer
    queryset = RankSportsPerson.objects.all()
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve rank for auth user."""
        return self.queryset.order_by('-id')


class TeamViewSet(viewsets.ModelViewSet):
    """View for manage team APIs."""
    serializer_class = serializers.TeamSerializer
    queryset = Team.objects.all()
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve team for auth user."""
        return self.queryset.order_by('-id')
