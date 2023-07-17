from mimesis.actions.actions import Action
from mimesis.agent.agent import Agent
import logging

class Reply(Action):
    name: str = "Read"
    description: str = "Just reply to the prompt given"
    definition: str = """Read"""
    prompt: str = ""

    def memory(self, agent: Agent) -> str:
        return "Prompt"

    def do(self, agent: Agent) ->  str:
        logging.warning(f"Prompt")
        return f"""{self.prompt}"""