"""
Admin customization for condition of point.
"""
from django.contrib import admin
from condition_point import models

admin.site.register(models.ConditionPoint)
