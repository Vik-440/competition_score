""""Serializers for sports_person APIs"""

from rest_framework import serializers
from django_filters import DateFilter
import django_filters
import re

from sports_person.models import SportsPerson


def normalize_fields(data, fields_to_normalize):
    """Normalize data for product"""
    for field in fields_to_normalize:
        if field in data:
            data[field] = ' '.join(
                [word.capitalize() for word in data[field].split(' ')])
            data[field] = re.sub(
                r"\'([A-Za-zА-Яа-я0-9])",
                lambda m: "'" + m.group(1).lower(),
                data[field]
            )
            data[field] = re.sub(
                r"\-([A-Za-zА-Яа-я0-9])",
                lambda m: "-" + m.group(1).capitalize(),
                data[field]
            )
    return


class SportsPersonFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(
        field_name='city', lookup_expr='icontains')
    team = django_filters.CharFilter(
        field_name='team', lookup_expr='icontains')
    last_name = django_filters.CharFilter(
        field_name='last_name', lookup_expr='icontains')
    rank = django_filters.CharFilter(
        field_name='rank', lookup_expr='icontains')
    born_after = DateFilter(field_name='birth_day', lookup_expr='gte')
    born_before = DateFilter(field_name='birth_day', lookup_expr='lte')

    class Meta:
        model = SportsPerson
        fields = [
            'city', 'team', 'last_name', 'born_after', 'born_before', 'rank']


class SportsPersonSerializer(serializers.ModelSerializer):
    """Serializer for sports_person."""

    def to_internal_value(self, data):
        fields_to_normalize = ['first_name', 'last_name', 'city', 'team']
        normalize_fields(data, fields_to_normalize)
        return super().to_internal_value(data)

    class Meta:
        model = SportsPerson
        fields = [
            'id', 'first_name', 'last_name', 'birth_day',
            'rank', 'city', 'team',]
        read_only_fields = ['id']
