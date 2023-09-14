from django.db import models


class SportsPerson(models.Model):
    """SportsPerson object."""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_day = models.DateField()
    city = models.CharField(max_length=50, default=None)
    team = models.CharField(max_length=50, default=None)
    rank = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.last_name

    class Meta:
        unique_together = ('first_name', 'last_name', 'birth_day')
