from django.urls import path

from . import views

app_name = "agents"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:agent_id>/", views.detail, name="detail"),
]