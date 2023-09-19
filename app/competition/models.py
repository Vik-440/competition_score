""""DB for all competition in general"""

from django.db.models import (
    Model,
    CharField,
    DateField,
    IntegerField,
)
from django.core.validators import MinLengthValidator


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
        return f'{self.competition_name}, \
            {self.competition_city}, \
            {self.competition_date}-\
            {self.competition_date + self.competition_qty_days}'

    class Mete:
        unique_together = (
            'competition_name', 'competition_city', 'competition_date')
