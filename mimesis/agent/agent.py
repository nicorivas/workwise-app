from __future__ import annotations
import json
import logging
from typing import Literal, Union, Iterable

from pydantic import BaseModel

from mimesis.personality.personality import Personality
from mimesis.actions.actions import Action, Chain
from mimesis.memory.memory import Memory
from mimesis.thought import Thought
from mimesis.model import LLM
from mimesis.role.role import Role

class Agent(BaseModel):
    """Base Agent class"""
    name: str = "Agent"
    definition: str = f"You are {name}, an agent that can experience the virtual world."
    personality: Union[Personality, None] = None
    role: Union[Role, None] = None
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
    
    def prompt(self, definition:bool = True, action: Union[Action, None] = None) -> str:
        prompt = ""
        if self.personality is not None:
            prompt += f"\n\n{self.personality.prompt()}"
        if self.role is not None:
            prompt += f"\n\n{self.role.act}"
        if action is not None:
            prompt += f"\n\n{action.do(self)}"
        return prompt

    def do(self, action: Union[Chain, Action, None]) -> str:
        """Execeutes an action
        
        Args:
            actions (Union[list[Action], Action, None]): Action(s) to execute

        Returns:
            replies (list[dict[str,str]]): List of replies
        """
        if isinstance(action, Chain):
            # Chain of actions, redirect
            return self.do_chain(action)
        else:
            # Single action
            prompt = self.prompt(action=action)
            if action is not None:
                self.add_memory(Memory(description=action.memory))
            reply = {}
            text = self.llm.chat(self, prompt, self.definition)
            reply["text"] = text
            reply["type"] = action.reply.type
            reply["name"] = action.reply.name
            return [reply]
    
    def do_chain(self, chain: Chain):
        replies = []

        for i in range(len(chain.actions)):

            # Get action, given replies so far
            action = chain.get_action(i, replies[i-1] if len(replies) > 0 else None)

            # Get prompt of action
            prompt = self.prompt(action=action)

            # Create memory of action
            if action is not None:
                self.add_memory(Memory(description=action.memory(self)))
            
            # Call the LLM and store reply
            reply = {}
            text = self.llm.chat(self, prompt, self.definition)
            reply["text"] = text
            reply["name"] = action.reply_name
            reply["type"] = action.reply_type
            
            # Add reply to list of replies
            replies.append(reply)

        return replies

    
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
    
    def to_json(self, exclude_unset=True, exclude_none=True, indent=2, **kwargs):
        return super().model_dump_json(exclude_unset=exclude_unset, exclude_none=exclude_none, indent=indent, **kwargs)