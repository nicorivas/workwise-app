import time
import logging
from django.shortcuts import render, get_object_or_404
from django.views import View
from document.models import Document
from django.urls import reverse

class DocumentView(View):
    
    def get(self, request, document_id):
        print("DocumentView.get")
        document = get_object_or_404(Document, pk=document_id)
        context = {
            "document": document,
        }
        return render(request, "document/index.html", context)
    
class DocumentHeaderView(View):

    context = {}
    
    def get(self, request, document_id):
        print("DocumentHeaderView.get")
        self.get_document(document_id)
        return render(request, "document/header.html", self.context)
    
    def post(self, request, document_id):
        print("DocumentHeaderView.post",request.POST)
        self.get_document(document_id)
        
        # Forward
        forward_url_name = request.POST.get('forward_url_name')
        if forward_url_name:
            forward_url = reverse(request.POST.get('forward_url_name'),args=[document_id])
            forward_target = request.POST.get('forward_target')
            if forward_target:
                self.context["forward"] = {'url':forward_url, 'target':forward_target}
            else:
                logging.warning("No forward target given")
        else:
            logging.warning("No forward url given")

        return render(request, "document/header.html", self.context)
    
    def get_document(self, document_id):
        document = get_object_or_404(Document, pk=document_id)
        self.context = {
            "document": document,
        }
    
class DocumentBodyView(View):
    
    def get(self, request, document_id):
        print("DocumentBodyView.get")
        document = get_object_or_404(Document, pk=document_id)
        time.sleep(2)
        context = {
            "document": document,
        }
        return render(request, "document/body.html", context)