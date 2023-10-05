""""DB for all competition in general"""

from django.db.models import (
    Model,
    CharField,
    DateField,
    IntegerField,
)
from django.core.validators import MinLengthValidator
from datetime import timedelta


class Competition(Model):
    """Competition DB as performance in general"""

    competition_name = CharField(
        max_length=200,
        validators=[MinLengthValidator(10)]
    )
    competition_city = CharField(
        max_length=50,
        validators=[MinLengthValidator(3)],
    )
    competition_date = DateField()
    competition_qty_days = IntegerField()

    def __str__(self):
        end_date = self.competition_date + timedelta(
            days=self.competition_qty_days)
        return f'"id"={self.id}, {self.competition_name}, \
{self.competition_city}, {self.competition_date} - {end_date}'

    class Meta:
        unique_together = (
            'competition_name', 'competition_city', 'competition_date')
