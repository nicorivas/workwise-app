from django.urls import path

from .views import *

app_name = "task"

urlpatterns = [
    path("", task_index_view, name="index"),
    # CRUD
    #path("api/", document_index_json_view, name="index_json"),
    path("create/", task_create_view, name="create"),
    path("<int:task_id>/main", task_read_view, name="read"),
    path("<int:task_id>/", task_read_index_view, name="read_index"),
    path("<int:task_id>/delete", task_delete_view, name="delete"),
    # Read documents
    path("<int:task_id>/documents", task_read_documents_view, name="read_documents"),
    # Transcribe audio
    path('<int:project_id>/transcribe_audio/', transcribe_audio, name='transcribe_audio'),
]