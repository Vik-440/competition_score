"""Serializers for Nomination and conditions of them"""

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from django_filters import CharFilter, FilterSet
# import django_filters
# import re

from nomination.models import (
    Nomination,
    ConditionPerformance,
)


class NominationFilter(FilterSet):
    """Filter for Nomination"""
    nomination_name = CharFilter(
        field_name='nomination_name', lookup_expr='icontains')

    class Meta:
        model = Nomination
        fields = ['nomination_name',]


class NominationSerializer(ModelSerializer):
    """Serializer for Nomination"""
    competition_name = SerializerMethodField()

    def get_competition_name(self, obj: Nomination) -> str:
        return obj.competition_id.competition_name

    class Meta:
        model = Nomination
        fields = '__all__'
        read_only_fields = ['id', 'competition_name']


class ConditionPerformanceSerializer(ModelSerializer):
    """Serializer for condition create team for performance"""

    class Meta:
        model = ConditionPerformance
        fields = '__all__'
        read_only_fields = ['id']
