"""Views for SquadPoint APIs"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.db.models import Sum

from squad_point.models import SquadPoint
from squad_point.serializers import(
    SquadPointSerializer,
    SquadPointFilter,
    NominationResultSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class SquadPointViewSet(ModelViewSet):
    """View for manage SquadPoint APIs."""
    serializer_class = SquadPointSerializer
    queryset = SquadPoint.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = SquadPointFilter

    pagination_class = PageNumberPagination

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    paginator = PageNumberPagination()

    def get_queryset(self):
        """Retrieve SquadPoint API"""
        return self.queryset.order_by('-id')
    

class NominationResultsView(APIView):
    """View to retrieve squad results for a specific nomination"""
    pagination_class = StandardResultsSetPagination

    def get(self, request, nomination_id, *args, **kwargs):
        try:
            queryset = SquadPoint.objects.filter(squad_id__nomination_id=nomination_id)\
                                         .values('squad_id__squad_name')\
                                         .annotate(total_score=Sum('point'))\
                                         .order_by('-total_score')
            # results = [
            #     {
            #         'squad_name': item['squad_id__squad_name'],
            #         'total_score': item['total_score'],
            #     }
            #     for item in queryset
            # ]

            # paginator = self.pagination_class()
            # page = paginator.paginate_queryset(queryset, request)
            # if page is not None:
            #     return paginator.get_paginated_response(page)
            # return Response(results)
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)

            results = [
                {
                    'squad_name': item['squad_id__squad_name'],
                    'total_score': item['total_score'],
                }
                for item in page or queryset
            ]

            return paginator.get_paginated_response(results)
        except Exception as e:
            return Response({"error": str(e)}, status=500)