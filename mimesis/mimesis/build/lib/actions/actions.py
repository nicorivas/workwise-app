from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:  # Only imports the below statements during type checking
    from mimesis.agent.agent import Agent

from abc import abstractmethod
from typing import Any #Dict, List, Optional, Sequence, Tuple, Union

from pydantic import BaseModel

class Action(BaseModel):
    """Base Action class"""
    name: str
    description: str
    definition: str
    
    @abstractmethod
    def memory(self, agent: Agent, **kwargs: Any) -> str:
        """Get memory representation of action
        Args:
            **kwargs: User inputs.
        Returns:
            String, representing the memory, to be saved in agent's memory
        """

    @abstractmethod
    def do(self, agent: Agent, **kwargs: Any) -> str:
        """Execute the corresponding action
        Args:
            **kwargs: User inputs.
        Returns:
            TODO: Specify
        """