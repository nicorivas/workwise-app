import json

from pydantic import BaseModel

from mimesis.personality import Personality
from mimesis.actions.actions import Action
from mimesis.memory.memory import Memory
from mimesis.thought import Thought
from mimesis.model import LLM
from mimesis.role import Role

class Agent(BaseModel):
    """Base Agent class"""
    name: str = "Agent"
    definition: str = f"You are {name}, an agent that can experience the virtual world."
    personality: Personality | None = None
    role: Role | None = None
    memories: list[Memory] = []
    history: list[dict[str,str]] = []
    llm: LLM = LLM(log=True)

    def add_memory(self, memory: Memory):
        self.memories.append(memory)

    def delete_memory(self, memory: Memory):
        self.memories.remove(memory)

    def get_memory(self, index: int):
        return self.memories[index]
    
    def context(self) -> str:
        prompt = f"""{self.definition}\n
{self.personality}"""
        return prompt
    
    def prompt(self, definition:bool = True, action: Action | None = None) -> str:
        prompt = ""
        if definition:
            prompt = self.definition
        if self.personality is not None:
            prompt += f"\n\n{self.personality}"
        if self.role is not None:
            prompt += f"\n\n{self.role.act}"
        if action is not None:
            prompt += f"\n\n{action.do(self)}"
        return prompt

    def do(self, action: Action) -> str:
        prompt = self.prompt(action)
        
        self.add_memory(Memory(description=action.memory(self)))

        reply = self.llm.chat(self, prompt, self.definition)

        thoughts = [thought.split(":")[1].strip() for thought in reply.split("\n")]
        for thought in thoughts:
            self.add_memory(Thought(description=thought).memory)

        return "a"
    
    def history_register(self, message: dict[str,str]):
        """Register a message in the agent's history"""
        self.history.append(message)

    def save(self, filename: str):
        """Save agent state to file"""
        with open(filename, 'w') as f:
            f.write(self.json())

    def load(self, filename: str):
        """Load agent state from file"""
        with open(filename) as f:
            agent_json = json.load(f)
            self.name = agent_json["name"]
            self.definition = agent_json["definition"]
            if agent_json.get("personality"):
                self.personality = Personality(**agent_json["personality"])
            self.memories = [Memory(**memory) for memory in agent_json["memories"]]
            self.llm = LLM(**agent_json["llm"])
    
    def __str__(self) -> str:
        return self.name