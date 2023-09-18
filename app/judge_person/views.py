"""Views fro the judge person API."""

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
)

from judge_person.models import JudgePerson
from judge_person.serializers import (
    JudgePersonSerializer,
    JudgePersonFilter,
)


class StandardResultSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100


class JudgePersonViewSet(viewsets.ModelViewSet):
    """View for Judge Person APIs."""
    serializer_class = JudgePersonSerializer
    queryset = JudgePerson.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = JudgePersonFilter
    pagination_class = StandardResultSetPagination

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    paginator = PageNumberPagination()

    def get_queryset(self):
        """Retrieve judge_person for auth user."""
        return self.queryset.order_by('-id')

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
        unique_ranks = JudgePerson.objects.distinct('rank')
        unique_ranks_list = []
        for unique_rank in unique_ranks:
            unique_ranks_list.append(unique_rank.rank)

        return Response({'unique_ranks': unique_ranks_list})

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='rank',
                location=OpenApiParameter.QUERY,
                description='route for fast enter rank of exists sportsperson',
                required=True,
                type=str
            ),
        ],
        responses={
            200: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                name="Auto complete field for rank with answer",
                description="answer for query='r'",
                value={
                    "auto_complete_ranks": ["Master", "Junior"],
                },
                response_only=True
            ),
            OpenApiExample(
                name="empty answer",
                summary="Auto complete field for rank without answer",
                description="answer for query='poor' ",
                value={
                    "auto_complete_ranks": [],
                },
                response_only=True
            )
        ],
    )
    @action(detail=False, methods=['GET'])
    def autocomplete_ranks(self, request):
        """Getting relevant ranks from search_key"""
        query = request.GET.get('rank', '')
        relevant_ranks_list = []
        if query:
            relevant_ranks = JudgePerson.objects.filter(
                rank__icontains=query
            )
            for relevant_rank in relevant_ranks:
                relevant_ranks_list.append(relevant_rank.rank)
        return Response(
            {'auto_complete_ranks': list(set(relevant_ranks_list))},
            status=status.HTTP_200_OK
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='last_name',
                location=OpenApiParameter.QUERY,
                description='route for fast enter rank of exists judge_person',
                required=True,
                type=str
            ),
        ],
        responses={
            200: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                name="Auto complete field for last_name with answer",
                description="answer for query='r'",
                value={
                    "auto_complete_last_name": ["Obama", "Cruel"],
                },
                response_only=True
            ),
            OpenApiExample(
                name="empty answer",
                summary="Auto complete field for last_name without answer",
                description="answer for query='poor' ",
                value={
                    "auto_complete_last_name": [],
                },
                response_only=True
            )
        ],
    )
    @action(detail=False, methods=['GET'])
    def autocomplete_last_name(self, request):
        """Getting relevant last_name from search_key"""
        query = request.GET.get('last_name', '')
        relevant_last_name_list = []
        if query:
            relevant_last_name = JudgePerson.objects.filter(
                last_name__icontains=query
            )
            for relevant_last_name in relevant_last_name:
                relevant_last_name_list.append(relevant_last_name.last_name)
        return Response(
            {'auto_complete_last_name': list(set(relevant_last_name_list))},
            status=status.HTTP_200_OK
        )
