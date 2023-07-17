from pydantic import BaseModel
from datetime import datetime
from mimesis.memory.memory import Memory

class Thought(BaseModel):
    description:str
    time:datetime = datetime.now()

    @property
    def memory(self) -> Memory:
        return Memory(description=f"I thought: {self.description}")

    def __str__(self) -> str:
        return f"{self.time.strftime('%Y/%m/%d, %H:%M:%S')}: {self.description}"
