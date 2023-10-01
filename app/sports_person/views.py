"""Views for the sports_person APIs."""

from rest_framework import viewsets, status
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
)
from rest_framework.pagination import PageNumberPagination

from sports_person.models import SportsPerson, PersonRank
from sports_person import serializers


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PersonRankViewSet(viewsets.ModelViewSet):
    """View for manage sports_person APIs."""
    serializer_class = serializers.PersonRankSerializer
    queryset = PersonRank.objects.all()
    # filter_backends = [filters.DjangoFilterBackend]
    # filterset_class = serializers.SportsPersonFilter

    pagination_class = StandardResultsSetPagination

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    paginator = PageNumberPagination()

    def get_queryset(self):
        """Retrieve persons rank for auth user."""
        return self.queryset.order_by('person_rank_weight')


class SportsPersonViewSet(viewsets.ModelViewSet):
    """View for manage sports_person APIs."""
    serializer_class = serializers.SportsPersonSerializer
    queryset = SportsPerson.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = serializers.SportsPersonFilter

    pagination_class = StandardResultsSetPagination

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    paginator = PageNumberPagination()

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

    @extend_schema(
        responses={
            200: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                name="unique cities",
                value={
                    "unique_cities": ["Lviv", "Kyiv", "Test"],
                },
                response_only=True
            ),
        ],
    )
    @action(detail=False, methods=['GET'])
    def get_unique_cities(self, request):
        """Getting unique cities from DB sports_person."""
        unique_cities = SportsPerson.objects.distinct('city')
        unique_cities_list = []
        for unique_cities in unique_cities:
            unique_cities_list.append(unique_cities.city)

        return Response({'unique_cities': unique_cities_list})

    @extend_schema(
        responses={
            200: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                name="unique teams",
                value={
                    "unique_teams": ["Junior", "Abc", "Test"],
                },
                response_only=True
            ),
        ],
    )
    @action(detail=False, methods=['GET'])
    def get_unique_teams(self, request):
        """Getting unique teams from DB sports_person."""
        team = SportsPerson.objects.distinct('team')
        unique_teams_list = []
        for unique_team in team:
            unique_teams_list.append(unique_team.team)
        return Response({'unique_teams': unique_teams_list})

    @extend_schema(
        responses={
            200: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                name="unique ranks",
                value={
                    "unique_ranks": ["Master", "Junior", "no rank"],
                },
                response_only=True
            ),
        ],
    )
    @action(detail=False, methods=['GET'])
    def get_unique_ranks(self, request):
        """Getting unique ranks from DB sports_person."""
        unique_ranks = SportsPerson.objects.distinct('person_rank_id')
        unique_ranks_list = []
        for unique_rank in unique_ranks:
            unique_ranks_list.append(unique_rank.person_rank_id)

        return Response({'unique_ranks': unique_ranks_list})

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='team',
                location=OpenApiParameter.QUERY,
                description='route for fast enter name of exists team',
                required=True,
                type=str
            ),
        ],
        responses={
            200: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                name="Auto complete field for name team with answer",
                description="answer for query='jun' ",
                value={
                    "auto_complete_teams": ["Junior", "Jungle"],
                },
                response_only=True
            ),
            OpenApiExample(
                name="empty answer",
                summary="Auto complete field for name team without answer",
                description="answer for query='abc' ",
                value={
                    "auto_complete_teams": [],
                },
                response_only=True
            )
        ],
    )
    @action(detail=False, methods=['GET'])
    def autocomplete_teams(self, request):
        """Getting relevant teams from search_key"""
        query = request.GET.get('team', '')
        relevant_teams_list = []
        if query:
            relevant_teams = SportsPerson.objects.filter(
                team__icontains=query
            )
            for relevant_team in relevant_teams:
                relevant_teams_list.append(relevant_team.team)
        return Response(
            {'auto_complete_teams': list(set(relevant_teams_list))},
            status=status.HTTP_200_OK
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='city',
                location=OpenApiParameter.QUERY,
                description='route for fast enter name of exists city',
                required=True,
                type=str
            ),
        ],
        responses={
            200: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                name="Auto complete field for city with answer",
                description="answer for query='ky' ",
                value={
                    "auto_complete_teams": ["Kyiv", "Kyoto"],
                },
                response_only=True
            ),
            OpenApiExample(
                name="empty answer",
                summary="Auto complete field for city without answer",
                description="answer for query='abc' ",
                value={
                    "auto_complete_cities": [],
                },
                response_only=True
            )
        ],
    )
    @action(detail=False, methods=['GET'])
    def autocomplete_cities(self, request):
        """Getting relevant cities from search_key"""
        query = request.GET.get('city', '')
        relevant_cities_list = []
        if query:
            relevant_cities = SportsPerson.objects.filter(
                city__icontains=query
            )
            for relevant_city in relevant_cities:
                relevant_cities_list.append(relevant_city.city)
        return Response(
            {'auto_complete_cities': list(set(relevant_cities_list))},
            status=status.HTTP_200_OK
        )

    # @extend_schema(
    #     parameters=[
    #         OpenApiParameter(
    #             name='rank',
    #             location=OpenApiParameter.QUERY,
    #             description='route for fast enter rank',
    #             required=True,
    #             type=str
    #         ),
    #     ],
    #     responses={
    #         200: OpenApiTypes.OBJECT,
    #     },
    #     examples=[
    #         OpenApiExample(
    #             name="Auto complete field for rank with answer",
    #             description="answer for query='r'",
    #             value={
    #                 "auto_complete_ranks": ["Master", "Junior"],
    #             },
    #             response_only=True
    #         ),
    #         OpenApiExample(
    #             name="empty answer",
    #             summary="Auto complete field for rank without answer",
    #             description="answer for query='poor' ",
    #             value={
    #                 "auto_complete_ranks": [],
    #             },
    #             response_only=True
    #         )
    #     ],
    # )
    # @action(detail=False, methods=['GET'])
    # def autocomplete_ranks(self, request):
    #     """Getting relevant ranks from search_key"""
    #     query = request.GET.get('rank', '')
    #     relevant_ranks_list = []
    #     if query:
    #         relevant_ranks = SportsPerson.objects.filter(
    #             rank__icontains=query
    #         )
    #         for relevant_rank in relevant_ranks:
    #             relevant_ranks_list.append(relevant_rank.rank)
    #     return Response(
    #         {'auto_complete_ranks': list(set(relevant_ranks_list))},
    #         status=status.HTTP_200_OK
    #     )
