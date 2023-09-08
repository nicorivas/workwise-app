import json

from pydantic import BaseModel

from mimesis.personality.trait import Trait

class Personality(BaseModel):
    """Base Personality class
    
    Personalities are a collection of traits. These determine the thoughts that are generated from experiences.
    """
    traits: list[Trait] = []

    def load_traits(self, filename: str):
        """Given a filename of a json file, load traits into personality"""
        with open(filename) as f:
            traits_json = json.load(f)
            for trait in traits_json["traits"]:
                self.traits.append(Trait(**trait))

    def save(self, filename):
        """Save personality to JSON file"""
        with open(filename, "w") as f:
            f.write(self.json())
    
    @staticmethod
    def load(filename):
        """Load personality from JSON file"""
        personality = Personality()
        with open(filename) as f:
            personality_json = json.load(f)
            personality.traits = [Trait(**trait) for trait in personality_json["traits"]]
        return personality
    
    def prompt(self) -> str:
        str = f"""You have personality traits that define how you react and what you remember from experiences. Your personality traits are:\n"""
        str += "\n".join([f"* {trait.self_definition}" for trait in self.traits])
        return str