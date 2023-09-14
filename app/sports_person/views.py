"""Views for the sports_person APIs."""

from rest_framework import viewsets, status
from django_filters import rest_framework as filters
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
)
# from rest_framework.pagination import PageNumberPagination


from sports_person.models import SportsPerson
from sports_person import serializers


# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 100


class SportsPersonViewSet(viewsets.ModelViewSet):
    """View for manage sports_person APIs."""
    serializer_class = serializers.SportsPersonSerializer
    queryset = SportsPerson.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = serializers.SportsPersonFilter

    # pagination_class = StandardResultsSetPagination

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    # paginator = PageNumberPagination()

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
        return self.queryset.order_by('-id')

    @extend_schema(description=r'{"unique_cities": ["Lviv", "Kyiv", "Test"]}')
    @action(detail=False, methods=['GET'])
    def unique_cities(self, request):
        """Getting unique cities from DB sports_person."""
        unique_cities = SportsPerson.objects.distinct('city')
        unique_cities_list = []
        for unique_cities in unique_cities:
            unique_cities_list.append(unique_cities.city)

        return Response({'unique_cities': unique_cities_list})

    @extend_schema(description=r'{"unique_teams": ["Junior", "Abc", "Test"]}')
    @action(detail=False, methods=['GET'])
    def unique_teams(self, request):
        """Getting unique teams from DB sports_person."""
        unique_teams = SportsPerson.objects.distinct('team')
        unique_teams_list = []
        for unique_team in unique_teams:
            unique_teams_list.append(unique_team.team)

        return Response({'unique_teams': unique_teams_list})
