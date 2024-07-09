from django.db.models import (
    Model,
    CharField,
    IntegerField,
    AutoField,
)

from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
)


class ConditionPoint(Model):
    """Condition for points in nomination."""

    id = AutoField(primary_key=True)
    condition_name = CharField(
        max_length=100,
        validators=[MinLengthValidator(5)],
        null=False,
    )
    min_range_point = IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(250)],
        null=True,
    )
    max_range_point = IntegerField(
        default=250,
        validators=[MinValueValidator(0), MaxValueValidator(250)],
        null=True,
    )
    group_name = CharField(
        max_length=100,
        validators=[MinLengthValidator(5)],
        null=False,
    )
    description = CharField(
        default=None,
        max_length=1000,
        null=True,
    )
