import json
import pypandoc
import requests
from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.contrib.auth.models import User

from agents.models import Agent
from task.models import Task
from actions.models import Action

from langchain.text_splitter import MarkdownHeaderTextSplitter

import commonmark

class DocumentSource(models.Model):
    """A source of documents, i.e. Google Docs
    """
    index = models.IntegerField(default=0) # Default position of the element in any selector.
    name = models.CharField(max_length=256)
    icon = models.ImageField(upload_to="document_sources", null=True, blank=True)

    def __str__(self):
        return str(self.pk) + ". " + self.name

class DocumentElement(models.Model):
    """Element of a document
    """
    index = models.IntegerField(default=0) # Position of the element in the document.
    document = models.ForeignKey("Document", on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=True, blank=True)
    text = models.TextField()
    html = models.TextField(null=True, blank=True)
    markdown = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{str(self.pk)}. Document element ({self.title}), Document: {self.document}"
    
    @property
    def title_for_html(self):
        # Conver self title to a string that can be used as an id in html.
        if self.title == None:
            return ""
        elif isinstance(self.title, str):
            return self.title.replace(" ", "_").replace(".", "_").replace(",", "_").replace(":", "_").replace(";", "_").replace("?", "_").replace("!", "_").replace("(", "_").replace(")", "_").replace("[", "_").replace("]", "_").replace("{", "_").replace("}", "_").replace("/", "_").replace("\\", "_").replace("'", "_").replace('"', "_").replace("<", "_").replace(">", "_").replace("|", "_").replace("=", "_").replace("+", "_").replace("-", "_").replace("*", "_").replace("&", "_").replace("^", "_").replace("%", "_").replace("$", "_").replace("#", "_").replace("@", "_")
        else:
            return self.title

class Comment(models.Model):
    """Comment done by an agent to a document
    """
    document_element = models.ForeignKey(DocumentElement, on_delete=models.CASCADE, null=True, blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    text = models.TextField()
    consider = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk) + ". " + self.text

class Document(models.Model):

    class DocumentType(models.TextChoices):
        GENERAL = "GENE", _("General")
        PROJECT_CHARTER = "PRCH", _("Project Charter")
        FEEDBACK_GUIDELINE = "FBGD", _("Feedback Guideline")
        IMPORTED = "IMPO", _("Imported Document")

    source_choices = [
        ("google_docs", "Google Docs"),
        ("workwise", "WorkWise")
    ]

    # TODO: Documents should also keep the original reply from the model, before parsing to Markdown.
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=4, choices=DocumentType.choices, default=DocumentType.PROJECT_CHARTER)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True) # The task that this document belongs to
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, null=True, blank=True) # The project that this document belongs to
    version = models.IntegerField(default=1)
    author_agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True, blank=True) # The agent that created this document
    author_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # The user that created this document
    imported = models.BooleanField(default=False) # If the document was imported (contrary to documents created on the platform)
    source = models.CharField(max_length=64, null=True, blank=True, choices=source_choices) # Where does the document come from
    source_id = models.CharField(max_length=256, null=True, blank=True) # The id of the document at the source (i.e. Google Docs id)
    source_url = models.CharField(max_length=512, null=True, blank=True) # The url of the document at the source (i.e. the Google Docs url)
    reply = models.TextField(null=True, blank=True) # The text of the document
    json = models.JSONField(null=True, blank=True) # The json representation of the document
    sections = models.JSONField(null=True, blank=True) # The division of the document in sections
    is_format = models.BooleanField(default=False) # Whether this document is a format or not
    is_context = models.BooleanField(default=False) # Whether this document is a context or not
    date_published = models.DateTimeField(null=True, blank=True, default=datetime.now) # The date when the document was published
    parent_document = models.ForeignKey("Document", on_delete=models.CASCADE, null=True, blank=True) # The parent document of this document

    @staticmethod
    def markdown_to_json(markdown):
        """Convert markdown to json.

        Output json is formatted for editor.js.

        Markdown is initially converted to JSON representation of pandocs.
        Then pandocs JSON is converted to editor.js JSON.
        """

        def pandoc_block_content_extract_text(pandoc_block):
            """
            Text in pandoc blocks is represented as a list of elements inside "c" (content) elements.
            This function extracts the text from a list of elements.
            """
            text = ""
            #print("pandoc_block_content_extract_text", pandoc_block)
            for element in pandoc_block:
                #print("pandoc_block_content_extract_text", element)
                tn = ""
                if element["t"] == "Plain":
                    tn = pandoc_block_content_extract_text(element["c"])
                elif element["t"] == "Str":
                    tn = element["c"]
                elif element["t"] == "Space":
                    tn = " "
                elif element["t"] == "SoftBreak":
                    tn = "\n"
                elif element["t"] == "Quoted":
                    tn = "\""+pandoc_block_content_extract_text(element["c"][1])+"\""
                elif element["t"] == "Strong":
                    tn = "<b>"+pandoc_block_content_extract_text(element["c"])+"</b>"
                elif element["t"] == "BulletList":
                    tmp = pandoc_block_to_json_block(element)
                    if isinstance(tmp,dict):
                        tn = ",".join(tmp["data"]["items"])
                elif element["t"] == "RawInline":
                    tn = element["c"][1]
                #print(tn)
                #tn = tn.replace("<", "&lt;").replace(">", "&gt;")
                text += tn
            return text

        def pandoc_block_to_json_block(pandoc_block):
            """
            Given a pandoc block, determine the type, and then create a json block.
            """
            json_block = []
            #print("pandoc_block_to_json_block",pandoc_block["t"])
            if pandoc_block["t"] == "Header":
                json_block = [{
                    "id": i,
                    "type": "header",
                    "data": {
                        "text": pandoc_block_content_extract_text(pandoc_block["c"][2]),
                        "level": pandoc_block["c"][0]
                    }
                }]
            elif pandoc_block["t"] == "Para":
                json_block = [{
                    "id": i,
                    "type": "paragraph",
                    "data": {
                        "text": pandoc_block_content_extract_text(pandoc_block["c"])
                    }
                }]
            elif pandoc_block["t"] == "OrderedList":
                json_block = [{
                    "id": i,
                    "type": "list",
                    "data": {
                        "style": "ordered",
                        "items": [pandoc_block_content_extract_text(item) if len(item) > 0 else [] for item in pandoc_block["c"][1]]
                    }
                }]
            elif pandoc_block["t"] == "BulletList":
                json_block = [{
                    "id": i,
                    "type": "list",
                    "data": {
                        "style": "unordered",
                        "items": [pandoc_block_content_extract_text(item) if len(item) > 0 else [] for item in pandoc_block["c"]]
                    }
                }]
            return json_block

        # Convert markdown to pandoc json
        pandoc_json = json.loads(pypandoc.convert_text(markdown, 'json', format='md'))
        #print("pandoc_json")
        #print(pandoc_json)
        # Iterate over the root blocks of the pandoc json, parse each block, and add it to json_blocks.
        json_blocks = []
        for i, pandoc_block in enumerate(pandoc_json["blocks"]):
            json_blocks += pandoc_block_to_json_block(pandoc_block)

        # Construct final json
        json_final = {
            "time": 1614102734534,
            "blocks": json_blocks,
            "version": "2.19.0"
        }
        return json_final

    def clear_elements(self):
        print("Document.clear()")
        document_elements = DocumentElement.objects.filter(document=self)
        document_elements.delete()
        Comment.objects.filter(document_element__document=self).delete()

    def get_elements(self, sorted:bool=False):
        documentElements = DocumentElement.objects.filter(document=self)
        if sorted:
            documentElements = documentElements.order_by("index")
        return documentElements
    
    def create_elements_from_json(self):
        """Create documentElement objects from JSON description of document.
        We iterate over the blocks of the JSON and create elements in order.
        """
        documentElements = []
        current_element = -1

        # Structure of the JSON is given by EditorJS.
        # Blocks contain the data.
        blocks = json.loads(self.json)["blocks"]
        for block in blocks:
            if block["type"] == "header" and block["data"]["level"] == 2:
                current_element += 1
                # Create document element
                documentElements.append(DocumentElement(
                    index=current_element
                    ,document=self
                    ,text=block["data"]["text"]
                    ,title=block["data"]["text"]))
            if current_element != -1:
                if block["type"] == "paragraph":
                    documentElements[current_element].text += block["data"]["text"]+"\n\n"

        for documentElement in documentElements:
            print(documentElement.title)
            documentElement.save()

        return documentElements

    def create_elements_from_reply(self, reply, markdown=False):
        print("create_elements_from_reply")
        if markdown:
            
            markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("##","Section")])
            sections = markdown_splitter.split_text(reply)
            for i, section in enumerate(sections):
                content = section.page_content
                section = section.metadata.get("Section")
                if section:
                    text = "## " + section + "\n" + content
                else:
                    text = content
                html = commonmark.commonmark(text)
                de = DocumentElement(index=i, document=self, title=section, text=text, html=html, markdown=text)
                de.save()
        else:
            de = DocumentElement(document=self, text=reply, html=reply)
            de.save()
    
    def get_text(self):
        return self.text

    def create_format(self, name, text):
        print("Document.create_format", name)

        document = Document()
        document.name = name
        document.is_format = True
        document.parent_document = self
        document.task = self.task
        document.json = self.markdown_to_json(text)
        document.save()
        return document
    
    def update_format(self, document, format):
        action_parameters = {"document":document.text}
        reply = self.task.action.agent.do(f"mimesis/library/formats/{format.name}", action_parameters)
        document.json = self.markdown_to_json(reply["text"])
        document.save()

    def get_section(self, index):
        return self.sections[index]
    
    def get_section_title(self, index):
        print(json.loads(self.json)["blocks"][self.sections[index]["header"]["index"]])
        return json.loads(self.json)["blocks"][self.sections[index]["header"]["index"]]["data"]["text"]

    @property
    def text(self):

        if self.json:
            if isinstance(self.json, str):
                json_blocks = json.loads(self.json)
            else:
                json_blocks = self.json
            text = ""
            for i, block in enumerate(json_blocks["blocks"]):
                if block["type"] == "paragraph":
                    text += block["data"]["text"]+"\n\n"
                if block["type"] == "header":
                    text += "\n"
                    if block["data"]["level"] == 1:
                        text += "# "
                    elif block["data"]["level"] == 2:
                        text += "## "
                    elif block["data"]["level"] == 3:
                        text += "### "
                    elif block["data"]["level"] == 4:
                        text += "#### "
                    text += block["data"]["text"]+"\n\n"
                if block["type"] == "list":
                    text += "".join(["* "+item+"\n" for item in block["data"]["items"]])
            return text
        else:
            # Get all document elements
            document_elements = DocumentElement.objects.filter(document=self)
            # Join all texts
            text = ""
            for document_element in document_elements:
                text += document_element.text
            return text

    def __str__(self):
        return str(self.pk) + ". " + self.name