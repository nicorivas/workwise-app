from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    re_path("ws/openai_stream/", consumers.OpenAIConsumer.as_asgi()),
]