from django.contrib import admin

from .models import Agent
from .models import Personality
from .models import Trait

admin.site.register(Agent)
admin.site.register(Personality)
admin.site.register(Trait)