from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:  # Only imports the below statements during type checking
    from mimesis.agent.agent import Agent

from abc import abstractmethod
from typing import Any #Dict, List, Optional, Sequence, Tuple, Union
from mimesis.prompt.prompt import PromptTemplate
import tomllib

from pydantic import BaseModel

class ActionReply(BaseModel):
    type: str
    name: str

class Action(BaseModel):
    """Abstract Action class

    Args:
        name (str): Name of the action
        description (str): Description of the action
        definition (str): Definition of the action
        reply_type (str): Type of reply to be returned
        reply_name (str): Name of the reply to be returned
    """
    name: str
    description: str
    definition: str
    reply: ActionReply
    prompt: PromptTemplate
    memory: str

    @staticmethod
    def load_from_file(filename):
        with open(f"{filename}.toml", "rb") as f:
            config = tomllib.load(f)
        action = Action(**config)
        return action
    
    def do(self, agent: Agent, **kwargs: Any) -> str:
        """Execute the corresponding action
        Args:
            **kwargs: User inputs.
        Returns:
            TODO: Specify
        """
        return self.prompt.get_prompt(**kwargs)

class Chain(BaseModel):
    """Chain of actions

    Args:
        actions (list[Action]): List of actions
    """    
    
    actions: list[Action] = []
    replies: list[str] = []

    def add_action(self, action: Action) -> None:
        """Add an action to the chain
        Args:
            action (Action): Action to add
        Returns:
            actions (list[Action]): List of actions
        """
        self.actions.append(action)
        return self.actions
