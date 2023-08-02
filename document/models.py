import json

from django.db import models

from django.apps import apps

from agents.models import AgentDB

class DocumentElement(models.Model):
    """Element of a document
    """
    document = models.ForeignKey("Document", on_delete=models.CASCADE)
    text = models.TextField()
    html = models.TextField()
    markdown = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.text

class Comment(models.Model):
    """Comment done by an agent to a document
    """
    document_element = models.ForeignKey(DocumentElement, on_delete=models.CASCADE, null=True, blank=True)
    agent = models.ForeignKey(AgentDB, on_delete=models.CASCADE)
    text = models.TextField()
    consider = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Document(models.Model):
    # TODO: Maybe documents should also keep the original reply from the model, before parsing to Markdown.
    name = models.CharField(max_length=256)
    text = models.TextField()
    version = models.IntegerField(default=1)
    json = models.TextField(null=True, blank=True)

    def clear(self):
        DocumentElement.objects.filter(document=self).delete()
        Comment.objects.filter(document_element__document=self).delete()

    def create_element_from_reply(self, markdown=False):
        if markdown:
            de = DocumentElement(document=self, text=self.text, html=f"<p>{self.text}</p>", markdown=self.text)
            de.save()
        else:
            de = DocumentElement(document=self, text=self.text, html=self.text)
            de.save()


    def create_elements_from_json(self, comments=True):
        """Create document elements from json
        """
        agent = apps.get_model('projects.Project').objects.get(document=self.pk).agent
        for key, value in json.loads(self.json).items():
            if key == "title":
                text = value["text"]
                de = DocumentElement(document=self, text=text, html=f"<h1>{text}</h1>")
                de.save()
                if value.get("comments") and comments:
                    Comment(document_element=de, agent=agent, text=value["comments"]).save()
                    de.save()
            elif key == "main_objectives":
                DocumentElement(document=self, text=value, html=f"<h2>Main objectives</h2>").save()
                for objective in value:
                    text = objective["description"]
                    de = DocumentElement(document=self, text=text, html=f"<ul><li>{text}</li></ul>")
                    de.save()
                    if objective.get("comments") and comments:
                        Comment(document_element=de, agent=agent, text=objective["comments"]).save()
                        de.save()
            elif key == "background":
                text = value["text"]
                de = DocumentElement(document=self, text=text, html=f"<h2>Background</h2><p>{text}</p>")
                de.save()
                if value.get("comments") and comments:
                    Comment(document_element=de, agent=agent, text=value["comments"]).save()
                    de.save()
            elif key == "timeline":
                text = value["text"]
                de = DocumentElement(document=self, text=text, html=f"<h2>Timeline</h2><p>{text}</p>")
                de.save()
                if value.get("comments") and comments:
                    Comment(document_element=de, agent=agent, text=value["comments"]).save()
                    de.save()
            elif key == "stakeholders":
                de = DocumentElement(document=self, text=text, html=f"<h2>Stakeholders</h2>")
                de.save()
                for stakeholder in value:
                    name = stakeholder["name"]
                    role = stakeholder["role"]
                    de = DocumentElement(document=self, text=stakeholder, html=f"<ul><li>{name}: {role}</li></ul>")
                    de.save()
                    if stakeholder.get("comments") and comments:
                        Comment(document_element=de, agent=agent, text=stakeholder["comments"]).save()
                        de.save()
            elif key == "risks_and_assumptions":
                de = DocumentElement(document=self, text=value, html=f"<h2>Risks & Assumptions</h2>")
                de.save()
                for risk in value:
                    type = risk["type"]
                    description = risk["description"]
                    de = DocumentElement(document=self, text=risk, html=f"<ul><li>{type}: {description}</li></ul>")
                    de.save()
                    if risk.get("comments") and comments:
                        Comment(document_element=de, agent=agent, text=risk["comments"]).save()
                        de.save()
    
    def __str__(self):
        return self.name