from django.urls import path

from .views import *

app_name = "actions"

urlpatterns = [
    path("", ActionsView.as_view(), name="index"),
    path("<int:action_id>/", ActionReadView.as_view(), name="read"),
    path("<int:action_id>/prompts", ActionReadPromptsView.as_view(), name="prompts"),
    path("<int:action_id>/instructions", ActionReadInstructionTypesView.as_view(), name="read_instruction_types"),
    path("<int:action_id>/instructions/create/", ActionInstructionsCreateView.as_view(), name="create_instruction"),
    path("<int:action_id>/test", ActionCallView.as_view(), name="action_call"),
]