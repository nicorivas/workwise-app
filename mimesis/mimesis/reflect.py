from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:  # Only imports the below statements during type checking
    from mimesis.agent.agent import Agent

from mimesis.actions.actions import Action
import logging

class Reflect(Action):

    name: str = "reflect"
    description: str = "Reflect over memories"
    definition: str = "You can reflect. When you reflect, you convert a list of memories into a thought. The thought is related to the memories. It takes into account which memory resonates the most with your personality. You should always write the thought in the following format: Thought: 'thought'. You should always provide only one thought."

    def memory(self, agent: Agent) -> str:
        """Memory representation of a reflection"""
        return f"I reflected over {len(agent.memories)} memories"

    def do(self, agent: Agent) ->  str:
        logging.warning(f"Reflecting over {len(agent.memories)} memories")
        
        memories_str: str = '\n'.join([str(a) for a in agent.memories])

        return f"""{self.definition}.
        
        Reflect over the following list of memories, delimited by triple equals:
        ===
        {memories_str}
        ===
        """