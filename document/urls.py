from django.urls import path

from .views import DocumentView, DocumentHeaderView, DocumentBodyView

app_name = "document"

urlpatterns = [
    path("<int:document_id>/", DocumentView.as_view(), name="document"),
    path("<int:document_id>/header/", DocumentHeaderView.as_view(), name="document_header"),
    path("<int:document_id>/body/", DocumentBodyView.as_view(), name="document_body"),
]