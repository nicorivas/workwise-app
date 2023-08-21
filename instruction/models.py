from django.db import models

from projects.models import Project
from actions.models import Action

from langchain.text_splitter import MarkdownHeaderTextSplitter

import commonmark

class MessageBlock(models.Model):
    """A MessageBlock is a block of text that belongs to a Message. It contains replies from the agent.
    """
    message = models.ForeignKey("Message", on_delete=models.CASCADE)
    text = models.TextField(default="", null=True, blank=True)
    html = models.TextField(default="", null=True, blank=True)
    selectable = models.BooleanField(default=True)
    selected = models.BooleanField(default=True)

    def generate_html(self):
        self.html = commonmark.commonmark(self.text)

    def __str__(self):
        return self.text

class Message(models.Model):
    """A Message is a container of MessageBlocks.

    Attributes:
        instruction (Instruction): The instruction that this message belongs to.
        user (str): The user that sent the message.
        type (str): The type of the message.
    """
    instruction = models.ForeignKey("Instruction", on_delete=models.CASCADE)
    user = models.CharField(max_length=256, null=True, blank=True)
    type = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.message
    
    def get_text(self):
        # Get all message blocks
        blocks = MessageBlock.objects.filter(message=self)
        text = ""
        for block in blocks:
            if block.selected:
                text += block.text + "\n"
        return text
    
    def set_text(self, text):
        headers_to_split_on = [
            ("##", "Section"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        md_header_splits = markdown_splitter.split_text(text)
        for section_obj in md_header_splits:
            content = section_obj.page_content
            section = section_obj.metadata.get("Section")
            if section:
                text = "## " + section + "\n" + content
            else:
                text = content
            block = MessageBlock.objects.create(message=self, text=text)
            block.generate_html()
            block.save()

class InstructionType(models.Model):
    """An InstructionType is a step of an Action. It is a container of ActionElements, and it's main function is to stablish dependencies of flow in the action.

    Attributes:
        name (str): The name of the instruction.
        action (Action): The action that this instruction belongs to.
        previous_instruction (Instruction): The previous instruction that this instruction depends on.
    """
    name = models.CharField(max_length=255)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    previous_instruction = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Instruction Type {self.pk}: {self.name}"
    
    def get_possible_actions(self):
        if self.previous_instruction:
            return self.previous_instruction.action.get_next_actions()
        else:
            return Action.objects.filter(previous_action=None)


class Instruction(models.Model):
    """An instruction is a step of an action. It is a container to stablish the logic between the different steps.

    Attributes:
        name (str): The name of the instruction.
        action (Action): The action that this instruction belongs to.
        project (Project): The project that this instruction belongs to.
    """
    type = models.ForeignKey(InstructionType, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    finished = models.BooleanField(default=False)
    previous_instruction = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Instruction: {self.pk}, Type: {self.type.name if self.type else 'None'}"
    
    def delete_messages(self):
        Message.objects.filter(instruction=self).delete()

    def add_message(self, text):
        message = Message.objects.create(instruction=self)
        message.set_text(text)
        message.save()

    def get_possible_actions(self):
        if self.previous_instruction:
            return self.previous_instruction.action.get_next_actions()
        else:
            return Action.objects.filter(previous_action=None)
