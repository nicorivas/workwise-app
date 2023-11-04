from django.shortcuts import render
from django.views import View

from document.models import Document
from document.forms import LoaderGoogleDocsForm

class LoaderGoogleDocsReadView(View):

    def get(self, request):
        print("GoogleDocsReadView.get")
        context = {"form":LoaderGoogleDocsForm}
        return render(request, "document/loader/google_docs.html", context)

class LoaderGoogleDocsLoadView(View):

    def post(self, request):
        print("DocumentLoadGoogleView.post")

        print(request.POST)

        form = LoaderGoogleDocsForm(request.POST)
        if form.is_valid():
            from llama_index import download_loader
            
            # Load document from Google Docs
            document_id = form.cleaned_data["document_id"]
            li_GoogleDocsReader = download_loader('GoogleDocsReader')
            li_loader = li_GoogleDocsReader()
            google_docs_ids = [document_id]
            li_documents = li_loader.load_data(document_ids=google_docs_ids)
            
            for li_document in li_documents:
                # Create document
                document = Document(
                    name = "Google Docs Document",
                    type = Document.DocumentType.IMPORTED,
                    author_user = request.user,
                    imported = True,
                    source = "google_docs",
                    source_id = document_id
                )
                document.save()
                document.create_elements_from_reply(li_document.get_content())


            # Save document representation to vector store

            print(li_documents)
        
        
        
        
        
        
        