""""Views for the Competition APIs."""

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
)
from collections import defaultdict
from datetime import datetime, timedelta

from competition.models import Competition
from competition.serializers import (
    CompetitionSerializer,
    CompetitionFilter,
)
from squad.models import Squad
from squad_person.models import SquadPerson
from user.permissions import IsSuperuser, IsStaff, IsCoach, IsJudge, IsObserver


class StandardResultSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100


class CompetitionViewSet(viewsets.ModelViewSet):
    """View for Competition APIs."""
    serializer_class = CompetitionSerializer
    queryset = Competition.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompetitionFilter
    pagination_class = StandardResultSetPagination

    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    paginator = PageNumberPagination()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy', 'check_period_person_performance']:
            permission_classes = [IsStaff]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='competition_id',
                location=OpenApiParameter.QUERY,
                description='ID of competition',
                required=True,
                type=int
            ),
            OpenApiParameter(
                name='time_period',
                location=OpenApiParameter.QUERY,
                description='time for sport person between performance',
                required=True,
                type=int
            ),
        ],
        responses={
            200: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                name="Auto complete field for name team with answer",
                description="answer for query='jun' ",
                value=  {
                    "sport_person_id": 9,
                    "time_problem": [
                    {
                        "squad_id_1": 2,
                        "performance_date_time_1": "2024-03-11 08:03",
                        "squad_id_2": 6,
                        "performance_date_time_2": "2024-03-11 08:12"
                    },
                    {
                        "squad_id_1": 6,
                        "performance_date_time_1": "2024-03-11 08:12",
                        "squad_id_2": 7,
                        "performance_date_time_2": "2024-03-11 08:15"
                    }
                    ]
                },
                response_only=True
            )
        ],
    )
    @action(detail=False, methods=['GET'])
    def check_period_person_performance(self, request: int = 1, period_sec: int = 3000):
        """Check time period between performances of a person in different teams"""
        competition_id = request.GET.get('competition_id', '')
        period_sec = request.GET.get('time_period', '')

        competition = get_object_or_404(Competition, id=competition_id)
        squads = Squad.objects.filter(nomination_id__competition_id=competition)

        squad_persons = SquadPerson.objects.filter(squad_id__in=squads)

        times = defaultdict(list)

        for squad_person in squad_persons:
            person_id = squad_person.sports_person_id.id
            squad_id = squad_person.squad_id.id
            performance_date_time = squad_person.squad_id.performance_date_time.strftime("%Y-%m-%d %H:%M")

            times[person_id].append({
                "squad_id": squad_id,
                "performance_date_time": performance_date_time,
            })

        final_result = []

        for person_id, performances in times.items():
            performances.sort(key=lambda x: datetime.strptime(x['performance_date_time'], '%Y-%m-%d %H:%M'))

            for i in range(1, len(performances)):
                current_time = datetime.strptime(performances[i]['performance_date_time'], '%Y-%m-%d %H:%M')
                previous_time = datetime.strptime(performances[i - 1]['performance_date_time'], '%Y-%m-%d %H:%M')

                if (current_time - previous_time).total_seconds() < int(period_sec):

                    final_result.append({
                        "sport_person_id": person_id,
                        "time_problem": [{
                            'squad_id_1': performances[i - 1]['squad_id'],
                            'performance_date_time_1': performances[i - 1]['performance_date_time'],
                            'squad_id_2': performances[i]['squad_id'],
                            'performance_date_time_2': performances[i]['performance_date_time'],
                        }]
                    })
                    
        if final_result:
            return Response(
            final_result,
            status=status.HTTP_200_OK)

        return Response(
            {'performances': 'OK'},
            status=status.HTTP_200_OK)

    def get_queryset(self):
        # return self.queryset.order_by('-competition_date').reverse()
        return self.queryset.order_by('-id')
