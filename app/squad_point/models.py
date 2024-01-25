"""DB for Squad cross JudgePerson for and collect points by performance"""

from django.db.models import (
    Model,
    ForeignKey,
    DecimalField,
    IntegerField,
    CASCADE,
)
from django.core.validators import(
    MinValueValidator,
    MaxValueValidator,
)
from judge_person.models import JudgePerson
from squad.models import Squad


class SquadPoint(Model):
    """Table for points by performance"""
    squad_id = ForeignKey(Squad, on_delete=CASCADE, null=False)
    judge_person_id = ForeignKey(JudgePerson, on_delete=CASCADE, null=False)
    point = IntegerField(
        null=False,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )

    class Meta:
        unique_together = ('squad_id', 'judge_person_id')
