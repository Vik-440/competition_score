"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from django.contrib import admin
from django.urls import path, include
# from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),

    path('api/user/', include('user.urls')),
    path('api/', include('sports_person.urls')),
    path('api/judge_person/', include('judge_person.urls')),
    path('api/competition/', include('competition.urls')),
    path('api/', include('nomination.urls')),
    path('api/', include('squad.urls')),
    path('api/', include('squad_person.urls')),
    path('api/', include('squad_point.urls')),
    path('api/', include('condition_point.urls')),
    path('api/', include('community.urls')),
    # path('api/', include('user_community.urls')),
]
