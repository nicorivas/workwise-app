from django.urls import path

from .views import ChatReadView

app_name = "chat"

urlpatterns = [
    path("<int:agent_id>/", ChatReadView.as_view(), name="read"),
]