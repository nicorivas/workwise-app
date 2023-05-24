from abc import abstractmethod
from typing import Any #Dict, List, Optional, Sequence, Tuple, Union

from pydantic import BaseModel

class Trait(BaseModel):
    """Base Action class"""
    name: str
    category: str
    description: str
    self_definition: str
    examples: list[str] = []

    def __str__(self) -> str:
        return self.self_definition