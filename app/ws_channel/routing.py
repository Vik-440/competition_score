from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/competition_schedule/$', consumers.Consumer.as_asgi()),
]