from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "agents"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:agent_id>/", views.detail, name="detail"),
    path("<int:agent_id>/check_project/<int:project_id>", views.check_project, name="check_project"),
    path("<int:agent_id>/search/action/<int:action_id>/guide/", views.search_action_guide, name="search_action_guide"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)