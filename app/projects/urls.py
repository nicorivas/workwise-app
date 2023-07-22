from django.urls import path

from . import views

app_name = "projects"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:project_id>/", views.project, name="project"),
    path('<int:project_id>/transcribe_audio/', views.transcribe_audio, name='transcribe_audio'),
    path('<int:project_id>/call_action/', views.call_action, name='action'),
    path('<int:project_id>/gatekeeper/', views.gatekeeper, name='gatekeeper'),
    path('<int:project_id>/actions/', views.actions, name='actions'),
    path('<int:project_id>/select_action/<int:action_id>', views.select_action, name='select_action'),
]