from django.urls import path

from prompt.views import *

app_name = "prompt"
urlpatterns = [
    path("", prompt_index_view, name="index"),
    path("<int:prompt_id>/", prompt_read_view, name="read"),
    path("create/", prompt_create_view, name="create"),
]