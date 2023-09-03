"""
Django admin customization sports_person.
"""
from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.utils.translation import gettext_lazy as _

from sports_person import models

admin.site.register(models.SportsPerson)
