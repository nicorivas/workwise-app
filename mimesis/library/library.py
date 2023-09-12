import os
from pathlib import Path

from pydantic import BaseModel

class Library(BaseModel):

    def get_all():
        # Get all files in the library, return as list of dicts
        print([x for x in os.walk('./mimesis/library/')])
        templates = [[x[0]+"/"+y for y in x[2] if y.find(".toml")>0] for x in os.walk('./mimesis/library/')]
        templates = sum(templates, [])
        templates = [x.replace(".toml", "") for x in templates]
        print(templates)

        return [[x, x.split("/")[-1]] for i, x in enumerate(templates)]