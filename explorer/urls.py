from django.urls import path

from . import views

app_name = "explorer"
urlpatterns = [
    path("", views.index, name="index"),
    path("action_select/<int:action_id>", views.action_select, name="action_select"),
]