""""Serializers for sports_person APIs"""

from rest_framework import serializers

from sports_person.models import (
    SportsPerson,
    # RankSportsPerson,
    # City,
    # Team,
)


class SportsPersonSerializer(serializers.ModelSerializer):
    """Serializer for sports_person."""

    class Meta:
        model = SportsPerson
        fields = [
            'id', 'first_name', 'last_name',
            'birth_day', 'rank', 'city', 'team'
        ]
        read_only_fields = ['id']
