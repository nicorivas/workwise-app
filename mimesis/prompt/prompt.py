from pydantic import BaseModel
from jinja2 import Environment, BaseLoader, select_autoescape
import tomllib
from typing import Union

class PromptTemplate(BaseModel):

    text: str
    parameters: dict = {}

    def get_prompt(self, parameters:dict = {}) -> str:
        template = Environment(loader=BaseLoader()).from_string(self.text)
        prompt = template.render(self.parameters if parameters == {} else parameters)
        return prompt