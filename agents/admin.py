from django.contrib import admin

from .models import AgentDB
from .models import PersonalityDB
from .models import TraitDB

admin.site.register(AgentDB)
admin.site.register(PersonalityDB)
admin.site.register(TraitDB)