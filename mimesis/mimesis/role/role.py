from pydantic import BaseModel

class Role(BaseModel):
    """Role class
    
    Roles are stances taken over interpretation and communication of thoughts.
    """
    name: str
    act: str