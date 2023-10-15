"""Views for Nomination and Conditions APIs."""

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
# from django.core.serializers import serialize

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
)
from datetime import timedelta
from rest_framework.pagination import PageNumberPagination

from nomination.models import (
    Nomination,
    ConditionPerformance,
)
from nomination.serializers import (
    NominationSerializer,
    ConditionPerformanceSerializer,
    NominationFilter,
)
from squad.models import Squad


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class NominationViewSet(ModelViewSet):
    """View for manage Nomination APIs"""
    serializer_class = NominationSerializer
    queryset = Nomination.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = NominationFilter

    pagination_class = StandardResultsSetPagination

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    paginator = PageNumberPagination()

    def get_queryset(self):
        """Retrieve Nomination API"""
        return self.queryset.order_by('-id')

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='nomination_id',
                location=OpenApiParameter.QUERY,
                description='id nomination which must be sorted',
                required=True,
                type=int,
            ),
        ],
        responses={
            200: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                name='squads in nomination',
                value={'squads in nomination': [
                    {'squad_1': '2023-11-11T08:00:00'},
                    {'squad_2': '2023-11-11T08:05:00'},
                    {'squad_3': '2023-11-11T08:10:00'},
                    {'squad_4': '2023-11-11T08:15:00'},
                ]},
                response_only=True,
            ),
        ],
    )
    @action(detail=False, methods=['GET'])
    def squad_set_time(self, request):
        """Set time for squad, sorted and check time between
        performance each person"""
        nomination_id = request.GET.get('nomination_id', '')
        squad_to_sorted = Squad.objects.filter(nomination_id=nomination_id)
        nomination_data = Nomination.objects.get(id=nomination_id)
        performance_time = nomination_data.nomination_start_date_time

        time_delay_performance = timedelta(seconds=(
            nomination_data.performance_second +
            nomination_data.delay_between_performance_second))

        for squad in squad_to_sorted:
            squad.performance_date_time = performance_time
            performance_time += time_delay_performance

        Squad.objects.bulk_update(squad_to_sorted, ['performance_date_time'])

        # json_squad = json.loads(serialize('json', squad_to_sorted))
        tmp_list = []
        for squad in squad_to_sorted:
            tmp = {'squad_id': squad.id,
                   'squad_name': squad.squad_name,
                   'performance_date_time': (
                        squad.performance_date_time
                        .strftime("%Y-%m-%d %H:%M"))}
            tmp_list.append(tmp)
        return Response(
            tmp_list,
            status=status.HTTP_200_OK,
        )


class ConditionPerformanceViewSet(ModelViewSet):
    """View for manage Conditions of performance API"""
    serializer_class = ConditionPerformanceSerializer
    queryset = ConditionPerformance.objects.all()
    # filter_backends = [filters.DjangoFilterBackend]
    # filterset_class = serializers.SportsPersonFilter

    pagination_class = StandardResultsSetPagination

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    paginator = PageNumberPagination()

    def get_queryset(self):
        """Retrieve Conditions of performance API"""
        return self.queryset.order_by('-id')
