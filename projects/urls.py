from django.urls import path

from projects.views import *

app_name = "projects"
urlpatterns = [
    path("", project_index_view, name="index"),
    path("create", project_create_view, name="create"),
    path("<int:project_id>/", project_read_view, name="read"),
    path("<int:project_id>/update/name", update_name, name="update_name"), # TODO: This should be just update
    path("<int:project_id>/delete/", project_delete_view, name="delete"),

    # AJAX
    path("<int:project_id>/context/", project_context_view, name="context"),

    # Tasks
    path("<int:project_id>/tasks", project_read_view, name="read_tasks"),

    path('<int:project_id>/transcribe_audio/', transcribe_audio, name='transcribe_audio'),

    path('messages/<int:message_id>/delete', delete_message, name='delete_message'),
]