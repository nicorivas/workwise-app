from django.urls import path

from . import views

app_name = "projects"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:project_id>/", views.project, name="project"),
    path('<int:project_id>/transcribe_audio/', views.transcribe_audio, name='transcribe_audio'),
    path('<int:project_id>/instruction/<int:instruction_id>/call_action/<int:action_id>', views.call_action, name='call_action'),
    path('<int:project_id>/document/<int:document_id>', views.write_document, name='write_document'),
    path('<int:project_id>/gatekeeper/', views.gatekeeper, name='gatekeeper'),
    path('<int:project_id>/actions/', views.actions, name='actions'),
    path('<int:project_id>/select_action/<int:action_id>', views.select_action, name='select_action'),
    path('<int:project_id>/get_prompt/', views.get_prompt, name='get_prompt'),
    path('messages/<int:message_id>/delete', views.delete_message, name='delete_message'),
]