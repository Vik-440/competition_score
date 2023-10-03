"""
Django admin customization nomination and conditions.
"""
from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.utils.translation import gettext_lazy as _

from nomination import models

admin.site.register(models.Nomination)
admin.site.register(models.ConditionPerformance)
