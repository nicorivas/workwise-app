from django.urls import path

from .views import WriteProjectCharter, EvaluateProjectCharter

app_name = "actions"

urlpatterns = [
    path("<int:action_id>/project_charter/evaluate", EvaluateProjectCharter.as_view(), name="project_charter_evaluate"),
    path("<int:action_id>/project_charter/write", WriteProjectCharter.as_view(), name="project_charter_write"),
]