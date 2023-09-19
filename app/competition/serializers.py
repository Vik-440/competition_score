"""Serializer for Competition."""

from rest_framework.serializers import ModelSerializer
from django_filters import CharFilter, DateFilter, FilterSet
import re

from competition.models import Competition


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


class CompetitionFilter(FilterSet):
    """Filter for query search in DB Competition."""
    competition_name = CharFilter(
        field_name='competition_name',
        lookup_expr='icontains',
    )
    competition_city = CharFilter(
        field_name='competition_city',
        lookup_expr='icontains',
    )
    date_period_start = DateFilter(
        field_name='competition_date',
        lookup_expr='gte',
    )
    date_period_end = DateFilter(
        field_name='competition_date',
        lookup_expr='lte',
    )

    class Meta:
        model = Competition
        fields = [
            'competition_name',
            'competition_city',
            'date_period_start',
            'date_period_end'
        ]


class CompetitionSerializer(ModelSerializer):
    """Serializer for Competition."""

    def to_internal_value(self, data):
        fields_to_normalize = ['competition_city']
        normalize_fields(data, fields_to_normalize)
        return super().to_internal_value(data)

    class Meta:
        model = Competition
        fields = [
            'id',
            'competition_name',
            'competition_city',
            'competition_date',
            'competition_qty_days',
        ]
        read_only_fields = ['id']
