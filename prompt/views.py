from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404, redirect

from prompt.models import Prompt
from actions.models import Action

class PromptIndexView(View):

    def get(self, request):
        """Index view of projects, shows list.
        """
        print("PromptIndexView.get", request.GET)

        prompts = Prompt.objects.all()

        context = {
            "prompts":prompts
        }

        return render(request, "prompt/index.html", context)

prompt_index_view = PromptIndexView.as_view()

class PromptReadView(View):
    
    def get(self, request, prompt_id: int):
        """Read project, that is, show the main view of a project

        Args:
            request (HttpRequest): Django request object
            prompt_id (int): Prompt ID
        """
        print("PromptReadView.get", request.GET)

        prompt = get_object_or_404(Prompt, pk=prompt_id)

        context = {
            "prompt":prompt
        }

        return render(request, "prompt/prompt.html", context)

prompt_read_view = PromptReadView.as_view()

class PromptCreateView(View):
    
    def post(self, request):
        """Read project, that is, show the main view of a project

        Args:
            request (HttpRequest): Django request object
            prompt_id (int): Prompt ID
        """
        print("PromptCreateView.post", request.POST)

        action = get_object_or_404(Action, pk=request.POST.get("action"))

        prompt = Prompt(name="New prompt", created_by=request.user, updated_by=request.user)
        prompt.save()
        prompt.action.add(action)
        prompt.save()

        # Redirect to index
        return redirect("prompt:index")

prompt_create_view = PromptCreateView.as_view()