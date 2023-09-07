""""Serializers for sports_person APIs"""

from rest_framework import serializers
import django_filters

from sports_person.models import (
    SportsPerson,
    RankSportsPerson,
    City,
    Team,
)


class SportsPersonFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(
        field_name='city__city', lookup_expr='icontains')
    team = django_filters.CharFilter(
        field_name='team__team', lookup_expr='icontains')
    last_name = django_filters.CharFilter(
        field_name='last_name', lookup_expr='icontains')

    class Meta:
        model = SportsPerson
        fields = ['city', 'team', 'last_name']


class CitySerializer(serializers.ModelSerializer):
    """Serializer for city"""

    class Meta:
        model = City
        fields = ['id', 'city']
        read_only_fields = ['id']


class RankSerializer(serializers.ModelSerializer):
    """Serializer for rank"""

    class Meta:
        model = RankSportsPerson
        fields = ['id', 'rank']
        read_only_fields = ['id']


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for team"""

    class Meta:
        model = Team
        fields = ['id', 'team']
        read_only_fields = ['id']


class SportsPersonSerializer(serializers.ModelSerializer):
    """Serializer for sports_person."""

    city = serializers.SlugRelatedField(
        slug_field='city',
        queryset=City.objects,
        allow_null=True,
        required=False
    )

    class Meta:
        model = SportsPerson
        fields = [
            'id', 'first_name', 'last_name',
            'birth_day', 'rank',
            'city',
            'team',
        ]
        read_only_fields = ['id']

    def validate_first_name(self, value):
        """Validate and capitalize first_name."""
        return value.capitalize()

    def validate_last_name(self, value):
        """Validate and capitalize last_name."""
        return value.capitalize()
