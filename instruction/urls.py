from django.urls import path

# Instruction views
from .views.instruction import *
from .views.instruction_type import *
from .views.instruction_element import *
from .views.feedback import *

app_name = "instruction"
urlpatterns = [
    # Instruction index
    path("", instruction_index_view, name="index"),
    path("index/", instruction_index_view, name="index"),
    # Instruction CRUD
    path("create/", instruction_create_view, name="create"),
    path("<int:instruction_id>/", instruction_read_view, name="read"),
    path("<int:instruction_id>/update/", instruction_update_view, name="update"),
    path("<int:instruction_id>/delete/", instruction_delete_view, name="delete"),
    path("<int:instruction_id>/save/", instruction_save_view, name="save"),
    # Template
    path("create/from_template/<int:instruction_id>", instruction_create_from_template_view, name="create_from_template"),
    #path("template/<int:instruction_id>", InstructionReadTemplateView.as_view(), name="read_template"),
    # Message
    path("<int:message_id>/message/call", message_call_view, name="message_call"),
    # Message blocks
    #path('message_block/<int:message_block_id>/select', InstructionSelectMessageBlockView.as_view(), name='select_message_block'),
    # Feedback
    path("<int:instruction_id>/element/<int:instruction_element_id>/feedback", feedback_read_view, name="feedback_read"),
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
    path("<int:instruction_id>/element/<int:instruction_element_id>/transcribe", instruction_element_transcribe_view, name="element_transcribe"),
    path("<int:instruction_id>/element/<int:instruction_element_id>/call", instruction_element_call_view, name="element_call"),
    path("<int:instruction_id>/element/<int:instruction_element_id>/call_prompt", instruction_element_call_prompt_view, name="element_call_prompt"),
    path("<int:instruction_id>/element/<int:instruction_element_id>/revise", instruction_element_revise_view, name="element_revise"),
    path("<int:instruction_id>/element/<int:instruction_element_id>/revision_call", instruction_element_revision_call_view, name="element_revision_call"),
    path("<int:instruction_id>/element/<int:instruction_element_id>/feedback_call", instruction_element_feedback_call_view, name="element_feedback_call"),
    path("<int:instruction_id>/element/<int:instruction_element_id>/document_link", instruction_element_document_link_view, name="element_document_link"),
    path("document_link", instruction_element_document_link_view, name="element_document_link_link"),
    path("<int:instruction_id>/element/<int:instruction_element_id>/details", instruction_element_details_view, name="element_details"),
    # API
    path("api/instruction_element/create", instruction_element_create_api, name="api_element_create"),
]