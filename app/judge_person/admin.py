""""Django admin customization judge_person."""

from django.contrib import admin

from judge_person import models

admin.site.register(models.JudgePerson)
