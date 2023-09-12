from django.urls import path

# Instruction views
from .views.instruction import *
from .views.instruction_type import *
from .views.instruction_element import *

app_name = "instruction"
urlpatterns = [
    # Instruction index
    path("", instruction_index_view, name="index"),
    path("index/", instruction_index_view, name="index"),
    # Instruction CRUD
    path("create/", InstructionCreateView.as_view(), name="create"),
    path("<int:instruction_id>/", instruction_read_view, name="read"),
    path("update/<int:instruction_id>/", instruction_update_view, name="update"),
    path("delete/<int:instruction_id>/", InstructionDeleteView.as_view(), name="delete"),
    # Template
    #path("create/from_template/<int:instruction_id>", InstructionCreateFromTemplateView.as_view(), name="create_from_template"),
    #path("template/<int:instruction_id>", InstructionReadTemplateView.as_view(), name="read_template"),
    # Message blocks
    #path('message_block/<int:message_block_id>/select', InstructionSelectMessageBlockView.as_view(), name='select_message_block'),
    # Instruction type CRUD
    path("type/create/", instruction_type_create_view, name="type_create"),
    path("type/<int:instruction_type_id>/", instruction_type_read_view, name="type_read"),
    path("type/update/<int:instruction_type_id>/", instruction_type_update_view, name="type_update"),
    path("type/delete/<int:instruction_type_id>/", instruction_type_delete_view, name="type_delete"),
    # Instruction elements
    path("<int:instruction_id>/element/", instruction_element_index_view, name="element_index"),
    path("<int:instruction_id>/element/create", instruction_element_create_view, name="element_create"),
    path("<int:instruction_id>/element/<int:instruction_element_id>/read", instruction_element_read_view, name="element_read"),
    path("<int:instruction_id>/element/<int:instruction_element_id>/update", instruction_element_update_view, name="element_update"),
    path("<int:instruction_id>/element/<int:instruction_element_id>/delete", instruction_element_delete_view, name="element_delete"),
    path("<int:instruction_id>/element/<int:instruction_element_id>/call", instruction_element_call_view, name="element_call"),
    path("<int:instruction_id>/element/<int:instruction_element_id>/details", instruction_element_details_view, name="element_details"),
]