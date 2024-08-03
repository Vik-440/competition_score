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
from condition_point.models import ConditionPoint


class SquadPoint(Model):
    """Table for points by performance"""
    squad_id = ForeignKey(Squad, on_delete=CASCADE, null=False)
    judge_person_id = ForeignKey(JudgePerson, on_delete=CASCADE, null=False)
    point = IntegerField(
        null=False,
        validators=[MinValueValidator(0), MaxValueValidator(250)],
    )
    condition_point_id = ForeignKey(ConditionPoint, on_delete=CASCADE, null=False)

    def __str__(self):
        return f'"squad_id" = {self.squad_id}, "judge_person_id" = {self.judge_person_id}, \
"condition_point_id" = {self.condition_point_id}, "point" = {self.point}'

    class Meta:
        unique_together = ('squad_id', 'judge_person_id', 'condition_point_id')
