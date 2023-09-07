from django.db import models


class RankSportsPerson(models.Model):
    """List of ranks sports level - must be realize in future"""
    rank = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.rank


class City(models.Model):
    """List of cities - must be realize in future"""
    city = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.city


class Team(models.Model):
    """List of teams - must be realize in future"""
    team = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.team


class SportsPerson(models.Model):
    """SportsPerson object."""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_day = models.DateField()
    rank = models.ForeignKey(
        RankSportsPerson,
        on_delete=models.SET_NULL,
        null=True
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.last_name
