import json

from pydantic import BaseModel

from trait import Trait

class Personality(BaseModel):
    """Base Personality class"""
    traits: list[Trait] = []

    def load_traits(self, filename: str):
        """Given a filename of a json file, load traits into personality"""
        with open(filename) as f:
            traits_json = json.load(f)
            for trait in traits_json["traits"]:
                self.traits.append(Trait(**trait))

    def __str__(self) -> str:
        str = f"""You have personality traits that define how you react and what you remember from experiences. Your personality traits are:\n"""
        str += "\n".join([f"* {trait.self_definition}" for trait in self.traits])
        return str