from datetime import datetime

from django.db import models
from actions.models import Action
from projects.models import Project
from django.contrib.auth.models import User

class Task(models.Model):

    # Position in ordering
    index = models.IntegerField(null=True, blank=True)
    # Name of the task
    name = models.CharField(max_length=256)
    # Project associated
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # Action associated
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    # Active document
    active_document = models.ForeignKey('document.Document', on_delete=models.SET_NULL, null=True, blank=True, related_name="active_document")
    # Creation at
    created_at = models.DateTimeField(null=True, blank=True, default=datetime.now)
    # Updated at
    updated_at = models.DateTimeField(null=True, blank=True, default=datetime.now)
    # User who created the task
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.pk}. {self.name} ({self.project.name})"
    
    def get_active_document(self, format=False):
        """Get the active document for this task
        """
        if not format:
            if self.active_document.is_format:
                return self.active_document.parent_document
        return self.active_document
    
    @property
    def documents(self):
        """Get the documents associated with this task, ignoring formats
        """
        return self.document_set.exclude(is_format=True)
    
    @property
    def name_and_type(self):
        return f"{self.name} ({self.action.name})"