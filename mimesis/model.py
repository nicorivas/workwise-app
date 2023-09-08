from __future__ import annotations
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:  # Only imports the below statements during type checking
    from mimesis.agent.agent import Agent
from typing import Any
import openai
import logging
from pydantic import BaseModel

class LLM(BaseModel):

    API_KEY: str = "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"
    model: str = "gpt-3.5-turbo"
    #model: str = "gpt-4"
    log: bool = True

    def chat(self, agent: Agent, prompt: str, system: Union[str, None]) -> str:

        openai.api_key = self.API_KEY

        messages: list[dict[str,str]] = []
        if system:
            messages += [{"role": "system", "content": system}]
        messages += [{"role": "user", "content": prompt}]

        response: Any = openai.ChatCompletion.create(
            model=self.model,
            messages=messages
            )
        
        agent.history_register({"prompt":prompt,"response":response})

        reply: str = response["choices"][0]["message"]["content"]

        if self.log:
            log_msg = f"""== prompt ==\n{prompt}\n==reply==\n{reply}"""

        return reply