"""Views for the sports_person APIs."""

from rest_framework import viewsets, status
# from rest_framework import filters
from django_filters import rest_framework as filters
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import generics
from rest_framework.response import Response


from sports_person.models import SportsPerson
from sports_person import serializers


class SportsPersonViewSet(viewsets.ModelViewSet):
    """View for manage sports_person APIs."""
    serializer_class = serializers.SportsPersonSerializer
    queryset = SportsPerson.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = serializers.SportsPersonFilter

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        """Retrieve sports_person for auth user."""
        # return self.queryset.filter(user=self.request.user).order_by('-id')
        return self.queryset.order_by('-id')
