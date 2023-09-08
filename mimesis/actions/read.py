#
import logging
from typing import Literal, Union
from mimesis.actions.actions import Action
from mimesis.agent.agent import Agent
import mimesis.tools as tools
from pydantic import Json

class Read(Action):
    name: str = "Read"
    description: str = "General read action"
    definition: str = """You can read. When you read, you generate thoughts. Thoughts are brief sentences that relate your personality traits with the text that you are reading. You should always write thoughts in the following format: Thought: "thought". These are examples of thoughts:
* Thought: I find black holes very interesting, but I don't know much about them, I should read more.
* Thought: I wonder how people feel when dying, and if I could experience something similar.
"""

class Analyse(Action):
    name: str = "Analyse"
    description: str = "General analyse action"
    definition: str = """You can analyse. When you analyse, you generate ideas. You should always write ideas in the following format: Idea: idea. These are examples of ideas:
* Idea: I think this book is essential for the understanding of the human mind.
* Idea: The relation between unemployment and the real-state market is very complex.
"""
    url: str = ""

    def memory(self, agent: Agent) -> str:
        return f"I analyzed the following article: {self.url}"


    def do(self, agent: Agent) ->  str:
        logging.warning(f"Analysing website: {self.url}")
        article: str = scrape_text(self.url)
        return f"""{self.definition}

Analyse the following article, delimited by triple equal signs.
===
{article}
===
"""

class ReadWebsite(Read):

    name: str = "Website reader"
    description: str = "Website reader"
    url: str
    website: Union[str, None] = None
    title: Union[str, None] = None

    def memory(self, agent: Agent) -> str:
        if self.website == "theguardian":
            return f"I read the following article from The Guardian: {self.title}"
        else:
            return f"I read the following article: {self.url}"

    def do(self, agent: Agent) ->  str:
        article: str = scrape_text(self.url)
        return f"""{self.definition}

Read the following article, delimited by triple equal signs. After reading the article, provide an enumerated list of 5 thoughts:
===
{article}
===
"""

class ReadNewsHeadlines(Read):

    name: str = "News headline reader and selector"
    description: str = "News headline reader and selector"
    resulting_data: Union[Json, None] = None
    
    def memory(self, agent: Agent) -> str:
        return f"I checked news headlines"
        
    def do(self, agent: Agent) ->  str:
        headlines = tools.load_headlines()
        return f"""{self.definition}

The following is a list of news articles headlines. Read each of them and select the five that you find the most interesting. For each headline provide a thought. For example:
Headline: Who needs the Metaverse? Meet the people still living on Second Life
Thought: I find the idea of living in a virtual world very interesting.
===
{headlines.to_string(index=False, header=False, justify="left")}
===
"""

    def parse_reply(self, reply: str) -> None:
        print("parsing")
        print(reply)
        lines = reply.split("\n")
        print([line for line in lines if line.startswith("Headline:")])