from django.urls import path

from explorer.views import *

app_name = "explorer"
urlpatterns = [
    path("", index_view, name="index"),
    path("search/", explorer_search_view, name="search")
]