"""Serializers for conditions of points"""

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from django_filters import CharFilter, FilterSet

from condition_point.models import ConditionPoint


class ConditionPointFilter(FilterSet):
    """Filter for name of condition point."""
    condition_name = CharFilter(
        field_name='condition_name', lookup_expr='icontains')
    
    class Meta:
        model = ConditionPoint
        fields = ['condition_name']


class ConditionPointSerializer(ModelSerializer):
    """Serializer for condition point"""

    class Meta:
        model = ConditionPoint
        fields = '__all__'
        read_only_fields = ['id']