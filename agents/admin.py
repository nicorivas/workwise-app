from django.contrib import admin

# Register your models here.
from .models import AgentDB
from .models import PersonalityDB
from .models import TraitDB

admin.site.register(AgentDB)
admin.site.register(PersonalityDB)
admin.site.register(TraitDB)