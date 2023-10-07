"""Serializers for Squad cross SportsPerson"""

from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    ValidationError,
)
from datetime import timedelta

from squad_person.models import SquadPerson
from nomination.models import Nomination, ConditionPerformance
from sports_person.models import SportsPerson  # , PersonRank
from squad.models import Squad


# class SquadPersonSerializer(ModelSerializer):

#     class Meta:
#         model = SquadPerson
#         fields = '__all__'
#         read_only_fields = ['id']

# from rest_framework import serializers
# from .models import SquadPerson, Nomination, ConditionPerformance, PersonRank


class SquadPersonSerializer(ModelSerializer):
    squad_id = PrimaryKeyRelatedField(queryset=Squad.objects.all())
    sports_person_id = PrimaryKeyRelatedField(
        queryset=SportsPerson.objects.all())

    class Meta:
        model = SquadPerson
        exclude = ('id',)

    def validate(self, attrs):
        """
        Validate the SquadPerson data against the ConditionPerformance
        requirements.
        """

        # Get the current Nomination object.
        nomination = Nomination.objects.get(
            pk=attrs['squad_id'].nomination_id.pk)

        # Get the ConditionPerformance object for the current Nomination.
        condition_performance = ConditionPerformance.objects.get(
            nomination_id=nomination.pk)

        # Validate the gender.
        if (condition_performance.men_person and
                condition_performance.women_person):
            pass
        elif (condition_performance.men_person and not
                condition_performance.women_person):
            if attrs['sports_person_id'].gender != 'men':
                raise ValidationError(
                    {'sports_person_id': 'Only men are allowed in this squad.'}
                )
        elif (not condition_performance.men_person and
                condition_performance.women_person):
            if attrs['sports_person_id'].gender != 'women':
                raise ValidationError({
                    'sports_person_id': (
                        'Only women are allowed in this squad.')
                })
        else:
            raise ValidationError({'sports_person_id': 'Invalid gender.'})

        # Validate the age.
        if attrs['sports_person_id'].birth_day < (
            nomination.nomination_start_date_time - (timedelta(
                days=condition_performance.max_age_person * 365))):
            raise ValidationError({
                'sports_person_id': 'The sports person is too old.'})
        if attrs['sports_person_id'].birth_day > (
                nomination.nomination_start_date_time - timedelta(
                    days=condition_performance.min_age_person * 365)):
            raise ValidationError({'sports_person_id': (
                'The sports person is too young.')})

        # Validate the weight.
        if attrs['sports_person_id'].weight_kg < (
                condition_performance.min_weight_person):
            raise ValidationError({'sports_person_id': (
                'The sports person is too light.')})
        if attrs['sports_person_id'].weight_kg > (
                condition_performance.max_weight_person):
            raise ValidationError({'sports_person_id': (
                'The sports person is too heavy.')})

        # Validate the height.
        if attrs['sports_person_id'].height_cm < (
                condition_performance.min_height_person):
            raise ValidationError({'sports_person_id': (
                'The sports person is too short.')})
        if attrs['sports_person_id'].height_cm > (
                condition_performance.max_height_person):
            raise ValidationError({'sports_person_id': (
                'The sports person is too tall.')})

        # Validate the rank.
        if condition_performance.min_rank_person:
            if attrs['sports_person_id'].person_rank_id.pk < (
                    condition_performance.min_rank_person.pk):
                raise ValidationError({'sports_person_id': (
                    'The sports person\'s rank is too low.')})
        if condition_performance.max_rank_person:
            if attrs['sports_person_id'].person_rank_id.pk > (
                    condition_performance.max_rank_person.pk):
                raise ValidationError({'sports_person_id': (
                    'The sports person\'s rank is too high.')})

        return attrs
