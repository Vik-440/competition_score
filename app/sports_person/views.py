"""Views for the sports_person APIs."""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from sports_person.models import (
    SportsPerson,
    # RankSportsPerson,
    # City,
    # Team,
)
from sports_person import serializers


class SportsPersonViewSet(viewsets.ModelViewSet):
    """View for manage sports)person APIs."""
    serializer_class = serializers.SportsPersonSerializer
    queryset = SportsPerson.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve sports_person for auth user."""
        # return self.queryset.filter(user=self.request.user).order_by('-id')
        return self.queryset.order_by('-id')
