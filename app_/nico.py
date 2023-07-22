import json
import os
import logging

from typing import List

from mimesis.personality.personality import Personality
from mimesis.personality.trait import Trait
from mimesis.agent.agent import Agent
from mimesis.actions.read import ReadWebsite, ReadNewsHeadlines
from mimesis.reflect import Reflect

LOAD: bool = False
FILENAME = "nico.json"
FILEPATH = f"library/agents/{FILENAME}"

# check if file exists
if os.path.isfile(FILEPATH) and LOAD:
    with open(FILEPATH) as f:
        logging.warning("Loading agent from file")
        agent_json = json.load(f)
        agent = Agent(**agent_json)

else:

    personality = Personality()
    personality.load_traits('library/agents/traits.json')

    agent_name: str = "Nico"
    agent_definition: str = f"You are {agent_name}, an agent that can experience the virtual world."
    agent = Agent(name="Nico", definition=agent_definition, personality=personality)

readNewsHeadlines = ReadNewsHeadlines()
prompt = agent.prompt(action=readNewsHeadlines)
agent.do(readNewsHeadlines)
#print(prompt)

#url = "https://www.theguardian.com/technology/2023/jun/10/who-needs-the-metaverse-meet-the-people-still-living-on-second-life"
#readWebsite = ReadWebsite(url=url, website="theguardian")
#prompt = agent.prompt(action=readWebsite)
#print(prompt)
#agent.do(readWebsite)
#agent.save(FILEPATH)

#url = "https://www.theguardian.com/world/2023/may/06/sudans-warring-sides-to-begin-talks-in-saudi-arabia-as-fighting-rages-on"
#readWebsite = ReadWebsite(url=url, website="theguardian")
#agent.do(readWebsite)

#reflect = Reflect()
#agent.do(reflect)

#agent.save("nico.json")