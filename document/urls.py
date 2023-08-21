from django.urls import path

from .views import DocumentReadView, DocumentUpdateView, DocumentHeaderView, DocumentBodyView

app_name = "document"

urlpatterns = [
    path("<int:document_id>/", DocumentReadView.as_view(), name="read"),
    path("<int:document_id>/update/", DocumentUpdateView.as_view(), name="update"),
    path("<int:document_id>/header/", DocumentHeaderView.as_view(), name="document_header"),
    path("<int:document_id>/body/", DocumentBodyView.as_view(), name="document_body"),
    # HTMX
    path("<int:document_id>/refresh/", DocumentBodyView.as_view(), name="refresh"),
]