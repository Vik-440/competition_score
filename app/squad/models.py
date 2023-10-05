""""DB for Squad under Nomination"""

from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    DateTimeField,
    CASCADE,
)
from django.core.validators import MinLengthValidator

from nomination.models import Nomination


class Squad(Model):
    """Squad is table for to describe such temporary groups of athletes"""

    squad_name = CharField(
        max_length=200,
        validators=[MinLengthValidator(3)]
    )
    nomination_id = ForeignKey(Nomination, on_delete=CASCADE, null=False)
    performance_date_time = DateTimeField(
        default=None, blank=True, null=False
    )

    def save(self, *args, **kwargs):
        if not self.performance_date_time:
            self.performance_date_time = \
                self.nomination_id.nomination_start_date_time
        super().save(*args, **kwargs)

    def __str__(self):
        nomination_name = self.nomination_id.nomination_name
        return f'{nomination_name}, \
{self.squad_name} - {self.performance_date_time}'

    class Meta:
        unique_together = ('squad_name', 'nomination_id')
