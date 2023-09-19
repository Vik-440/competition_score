"""Django admin customization Competition"""

from django.contrib import admin

from competition import models

admin.site.register(models.Competition)
