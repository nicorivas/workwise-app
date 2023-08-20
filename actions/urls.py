from django.urls import path

from .views import EvaluateProjectCharter, ActionView, ActionsView, ActionCallView

app_name = "actions"

urlpatterns = [
    path("", ActionsView.as_view(), name="index"),
    path("<int:action_id>", ActionView.as_view(), name="action"),
    path("<int:action_id>/test", ActionCallView.as_view(), name="action_call"),
    path("<int:action_id>/project_charter/evaluate", EvaluateProjectCharter.as_view(), name="project_charter_evaluate"),
    #path("<int:action_id>/project_charter/write", WriteProjectCharter.as_view(), name="project_charter_write"),
]