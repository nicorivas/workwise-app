from pydantic import BaseModel
from datetime import datetime

class Memory(BaseModel):
    description:str
    time:datetime = datetime.now()

    def __str__(self) -> str:
        return f"{self.time.strftime('%Y/%m/%d, %H:%M:%S')}: {self.description}"
