from django.urls import path

from .views import *

app_name = "document"

urlpatterns = [
    path("", document_index_view, name="index"),
    # CRUD
    path("api/", document_index_json_view, name="index_json"),
    path("create/", DocumentCreateView.as_view(), name="create"),
    path("<int:document_id>/", DocumentReadView.as_view(), name="read"),
    path("<int:document_id>/update/", DocumentUpdateView.as_view(), name="update"),
    path("<int:document_id>/delete/", DocumentDeleteView.as_view(), name="delete"),
    # View
    path("<int:document_id>/view/", DocumentViewView.as_view(), name="view"),
    path("<int:document_id>/header/", DocumentHeaderView.as_view(), name="document_header"),
    path("<int:document_id>/body/", DocumentBodyView.as_view(), name="document_body"),
    # API
    path("api/v1/document/<int:document_id>/", DocumentReadApiView.as_view(), name="api_read"),
    path("api/v1/document/<int:document_id>/reply", DocumentReadReplyApiView.as_view(), name="api_read"),
    path("api/v1/document/<int:document_id>/save", DocumentSaveApiView.as_view(), name="api_save"),
    # AJAX/HTMX
    path("<int:document_id>/refresh/", DocumentBodyView.as_view(), name="refresh"),
    path("<int:document_id>/revise/", DocumentReviseView.as_view(), name="revise"),
    path("<int:document_id>/clear/", DocumentClearView.as_view(), name="clear"),
    path("<int:document_id>/format/", DocumentFormatView.as_view(), name="format"),
    path("<int:document_id>/sections/save", DocumentSectionsSaveView.as_view(), name="sections_save"),
    # Loaders
    # . Google
    path("load/google_docs/", LoaderGoogleDocsReadView.as_view(), name="loader_google_docs_read"),
    path("load/google_docs/load/", LoaderGoogleDocsLoadView.as_view(), name="loader_google_docs_load"),
]