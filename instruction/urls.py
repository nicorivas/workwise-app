from django.urls import path

from .views import InstructionReadView, InstructionCreateView, InstructionTypeReadView, InstructionSelectMessageBlockView

app_name = "instruction"
urlpatterns = [
    path("create/", InstructionCreateView.as_view(), name="create"),
    path("<int:instruction_id>/", InstructionReadView.as_view(), name="read"),
    path("type/<int:instruction_type_id>/", InstructionTypeReadView.as_view(), name="read_type"),
    path('message_block/<int:message_block_id>/select', InstructionSelectMessageBlockView.as_view(), name='select_message_block'),
]