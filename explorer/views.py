import os
import logging

from django.shortcuts import render, get_object_or_404

from projects.models import Project
from django.views import View
from agents.models import Agent
from actions.models import Action
from company.models import Company

def index_view(request):
    agents = Agent.objects.filter(show_in_explorer=True)
    # If we are part of a company, then filter by company
    company_id = request.session.get("company_id")
    if company_id:
        company = get_object_or_404(Company, pk=company_id)
        agents = agents.filter(company=company)
    else:
        if request.user.is_authenticated:
            company = request.user.profile.companies.first()
            if company:
                agents = agents.filter(company=company)
                request.session["company_id"] = company.pk
    actions = Action.objects.all()

    # Get default project
    default_project = Project.objects.filter(default=True).only("name").first()

    context = {
        "actions": actions,
        "agents": agents,
        "default_project":default_project
        }
    
    # We can access this either by index (direct hit to url) or by main (htmx load)
    if request.GET.get("source") == "menu":
        return render(request, "explorer/main.html", context)
    else:
        return render(request, "explorer/index.html", context)

class ExplorerSearchView(View):

    def post(self, request):
        """
        Semantic search of actions. We use LlamaIndex functions, Weaviate as Vector Store.

        Metadata and id's are set when the action descriptions are loaded.

        1. Get the vector store from Weaviate
        2. Create an index from the vector store
        3. Create a retriever from the index
        4. Retrieve the nodes
        5. Get the id of the actions from the metadata of the nodes.
        """
        import weaviate
        from llama_index import VectorStoreIndex
        from llama_index.vector_stores import WeaviateVectorStore
        
        query = request.POST.get("query")
        
        # Connect to Weaviate
        weaveiate_cluster_api_key = os.environ.get('WEAVEIATE_CLUSTER_API_KEY')
        weaveiate_cluster_url = os.environ.get('WEAVEIATE_CLUSTER_URL')
        auth_config = weaviate.AuthApiKey(api_key=weaveiate_cluster_api_key)
        weaviate_client = weaviate.Client(url=weaveiate_cluster_url, auth_client_secret=auth_config)
        vector_store = WeaviateVectorStore(weaviate_client=weaviate_client, index_name="Actions", text_key="content")
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

        # Get similar actions via retriever,
        # finding similarity between query and action description using llama_index
        retriever = index.as_retriever(similarity_top_k=10)
        nodes = retriever.retrieve(query)
        action_dicts = {}
        for node in nodes:
            id = node.metadata["workwise_id"]
            action_dicts[id] = {}
            action_dicts[id]["id"] = id
            action_dicts[id]["score"] = node.score

        # Get all actions retrieved, in order of relevance
        action_ids = [node.metadata["workwise_id"] for node in nodes]
        actions = list(Action.objects.filter(pk__in=action_ids))
        actions.sort(key=lambda x: action_dicts[x.pk]["score"], reverse=True)
        
        context = {
            "actions": actions
        }
        return render(request, "explorer/search_results.html", context)
    
explorer_search_view = ExplorerSearchView.as_view()