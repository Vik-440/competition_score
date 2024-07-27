"""Serializer for Squad cross JudgePerson"""

from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    CharField,
    IntegerField,
)
import django_filters

from squad_point.models import SquadPoint
from squad.models import Squad
from judge_person.models import JudgePerson


class SquadPointFilter(django_filters.FilterSet):
    """Filter for fields SquadPoint"""
    squad_id = django_filters.CharFilter(
        field_name='squad_id', lookup_expr='exact')
    judge_person_id = django_filters.CharFilter(
        field_name='judge_person_id', lookup_expr='exact')
    
    class Meta:
        model = SquadPoint
        fields = ['squad_id', 'judge_person_id']


class SquadPointSerializer(ModelSerializer):
    squad_id = PrimaryKeyRelatedField(queryset=Squad.objects.all())
    judge_person_id = PrimaryKeyRelatedField(
        queryset=JudgePerson.objects.all())
    
    class Meta:
        model = SquadPoint
        fields = '__all__'
        read_only_fields = ('id',)


class NominationResultSerializer(ModelSerializer):
    squad__squad_name = CharField()
    total_score = IntegerField()