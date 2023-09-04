from django.urls import path

# Instruction
from .views import InstructionIndexView, InstructionCreateView, InstructionReadView, InstructionDeleteView, InstructionReadPreviewView, InstructionCreateFromPreviewView
# InstructionTypes
from .views import InstructionTypeCreateView, InstructionTypeReadView
from .views import InstructionSelectMessageBlockView

app_name = "instruction"
urlpatterns = [
    # Instruction
    path("", InstructionIndexView.as_view(), name="index"),
    path("index/", InstructionIndexView.as_view(), name="index"),
    path("index/project/<int:project_id>/", InstructionIndexView.as_view(), name="index"),
    path("create/", InstructionCreateView.as_view(), name="create"),
    path("<int:instruction_id>/", InstructionReadView.as_view(), name="read"),
    path("delete/<int:instruction_id>/", InstructionDeleteView.as_view(), name="delete"),
    # Preview
    path("create/from_preview/<int:instruction_id>", InstructionCreateFromPreviewView.as_view(), name="create_from_preview"),
    path("preview/<int:instruction_id>", InstructionReadPreviewView.as_view(), name="read_preview"),
    # Message blocks
    path('message_block/<int:message_block_id>/select', InstructionSelectMessageBlockView.as_view(), name='select_message_block'),
    # Instruction types
    path("type/create/", InstructionTypeCreateView.as_view(), name="create_type"),
    path("type/<int:instruction_type_id>/", InstructionTypeReadView.as_view(), name="read_type"),
]