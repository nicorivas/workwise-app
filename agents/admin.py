from django.contrib import admin

from .models import Agent, Personality, Trait, AgentType

admin.site.register(AgentType)
admin.site.register(Agent)
admin.site.register(Personality)
admin.site.register(Trait)