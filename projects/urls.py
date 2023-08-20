from django.urls import path

from . import views

app_name = "projects"
urlpatterns = [
    path("", views.index, name="index"),
    path("new/<int:action_id>", views.new, name="new"),
    path("delete/<int:project_id>", views.delete, name="delete"),
    path("<int:project_id>/", views.project, name="project"),
    path('<int:project_id>/transcribe_audio/', views.transcribe_audio, name='transcribe_audio'),
    path('<int:project_id>/instruction/<int:instruction_id>/call_action/<int:action_id>', views.call_action, name='call_action'),
    path('<int:project_id>/instruction/<int:instruction_id>/end_action', views.end_action, name='end_action'),
    path('<int:project_id>/instruction/<int:instruction_id>/update', views.instruction_update, name='instruction_update'),
    path('<int:project_id>/instruction/<int:message_block_id>/select', views.select_message_block, name='select_message_block'),
    # Charter
    path('<int:project_id>/document/<int:document_id>/revise/<int:instruction_id>', views.revise_document, name='revise_document'),
    path('<int:project_id>/document/<int:document_id>/write/<int:instruction_id>', views.write_document, name='write_document'),
    path('<int:project_id>/document/<int:document_id>/apply_revision', views.apply_revision, name='apply_revision'),
    path('<int:project_id>/document/<int:document_id>/comment/<int:comment_id>/consider', views.comment_consider, name='comment_consider'),
    # Feedback
    path('<int:project_id>/feedback/<int:document_id>/feedback/<int:instruction_id>', views.feedback, name='feedback'),
    path('<int:project_id>/feedback/<int:document_id>/feedback_values/<int:instruction_id>', views.feedback_values, name='feedback_values'),
    #
    path('<int:project_id>/gatekeeper/', views.gatekeeper, name='gatekeeper'),
    path('<int:project_id>/actions/', views.actions, name='actions'),
    path('<int:project_id>/instruction/<int:instruction_id>/select_action/<int:action_id>', views.select_action, name='select_action'),
    path('<int:project_id>/get_prompt/', views.get_prompt, name='get_prompt'),
    path('messages/<int:message_id>/delete', views.delete_message, name='delete_message'),
]