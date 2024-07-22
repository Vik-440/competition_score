from django.db.models import (
    Model,
    CharField,
    IntegerField,
    ForeignKey,
    AutoField,
    DateTimeField,
    BooleanField,
    SET_NULL,
    CASCADE,
)
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
)
from sports_person.models import PersonRank
from competition.models import Competition

from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .tasks import notify_channel_layer
import json


class Nomination(Model):
    """Nomination object"""
    id = AutoField(primary_key=True)
    competition_id = ForeignKey(Competition, on_delete=CASCADE, null=False)
    nomination_name = CharField(
        max_length=100,
        validators=[MinLengthValidator(5)],
        null=False,
    )
    nomination_start_date_time = DateTimeField()
    performance_second = IntegerField()
    delay_between_performance_second = IntegerField()


# @receiver(post_save, sender=Nomination)
# def model_post_save(sender, instance, **kwargs):
#     notify_channel_layer(instance)
@receiver(post_save, sender=Nomination)
def model_post_save(sender, instance, created, **kwargs):
    if created:
        message = f'New nomination created: {instance}'
    else:
        message = f'Nomination updated: {instance}'

    notify_channel_layer(instance, message)

def notify_channel_layer(instance, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'nomination_group_info',
        {
            'type': 'update_message',
            'message': json.dumps({'id': instance.id, 'message': message})
        }
    )


class ConditionPerformance(Model):
    """Condition for create performance team"""
    id = AutoField(primary_key=True)
    nomination_id = ForeignKey(Nomination, on_delete=CASCADE, null=False)
    men_person = BooleanField(default=True)
    women_person = BooleanField(default=True)
    min_qty_person = IntegerField(
        default=None, null=True,
        validators=[MinValueValidator(0)]
    )
    max_qty_person = IntegerField(
        default=None, null=True,
        validators=[MinValueValidator(0)]
    )
    min_age_person = IntegerField(
        default=None,
        validators=[MinValueValidator(0), MaxValueValidator(250)],
        null=True,
    )
    max_age_person = IntegerField(
        default=None,
        validators=[MinValueValidator(0), MaxValueValidator(250)],
        null=True,
    )
    min_weight_person = IntegerField(
        default=None,
        validators=[MinValueValidator(1), MaxValueValidator(250)],
        null=True,
    )
    max_weight_person = IntegerField(
        default=None,
        validators=[MinValueValidator(1), MaxValueValidator(250)],
        null=True,
    )
    min_height_person = IntegerField(
        default=None,
        validators=[MinValueValidator(1), MaxValueValidator(250)],
        null=True,
    )
    max_height_person = IntegerField(
        default=None,
        validators=[MinValueValidator(1), MaxValueValidator(250)],
        null=True,
    )
    min_rank_person = ForeignKey(
        PersonRank,
        to_field='person_rank_name',
        related_name='min_rank_condition',
        on_delete=SET_NULL,
        null=True,
    )
    max_rank_person = ForeignKey(
        PersonRank,
        to_field='person_rank_name',
        related_name='max_rank_condition',
        on_delete=SET_NULL,
        null=True,
    )
