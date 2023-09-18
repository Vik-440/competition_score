"""URL mapping fro the JudgePerson app"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from judge_person.views import JudgePersonViewSet


router = DefaultRouter()
router.register('', JudgePersonViewSet)

app_name = 'judge_person'

urlpatterns = [
    path('', include(router.urls)),
]
