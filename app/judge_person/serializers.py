""""Serializers for judge person"""

from rest_framework import serializers
from django_filters import CharFilter, FilterSet
import re

from judge_person.models import JudgePerson


def normalize_fields(data, fields_to_normalize):
    """Normalize data for fields in Judge Person."""
    for field in fields_to_normalize:
        if field in data:
            data[field] = ' '.join(
                [word.capitalize() for word in data[field].split(' ')]
            )
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


class JudgePersonFilter(FilterSet):
    """Filter for query search in DB Judge Person."""
    last_name = CharFilter(
        field_name='last_name', lookup_expr='icontains'
    )
    rank = CharFilter(
        field_name='rank', lookup_expr='icontains'
    )
    team = CharFilter(
        field_name='team', lookup_expr='icontains'
    )

    class Meta:
        model = JudgePerson
        fields = [
            'last_name', 'rank', 'team',
        ]


class JudgePersonSerializer(serializers.ModelSerializer):
    """Serializers for Judge Person."""

    def to_internal_value(self, data):
        fields_to_normalize = [
            'first_name', 'last_name', 'team',
        ]
        normalize_fields(data, fields_to_normalize)
        return super().to_internal_value(data)

    class Meta:
        model = JudgePerson
        fields = [
            'id', 'first_name', 'last_name', 'birth_day',
            'rank', 'license_expiration_date', 'team',
        ]
        read_only_fields = ['id']
