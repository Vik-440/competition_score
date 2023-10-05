""""DB for Squad cross SportPerson"""

from django.db.models import (
    Model,
    ForeignKey,
    CASCADE,
)

from sports_person.models import SportsPerson
from squad.models import Squad


class SquadPerson(Model):
    """Table for crossing Squad and Sports Person"""

    squad_id = ForeignKey(Squad, on_delete=CASCADE, null=False)
    sports_person_id = ForeignKey(SportsPerson, on_delete=CASCADE, null=False)

    class Meta:
        unique_together = ('squad_id', 'sports_person_id')
