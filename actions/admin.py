from django.contrib import admin

from .models import Action#, ActionElement, ActionElementType

#admin.site.register(Action)

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'agent', 'description')
    pass
