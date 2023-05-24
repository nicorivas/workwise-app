import json
import os
import logging

from typing import List

from personality import Personality
from trait import Trait
from agent import Agent
from read import ReadWebsite
from reflect import Reflect

LOAD: bool = False

# check if file exists
if os.path.isfile('nico.json') and LOAD:
    with open('nico.json') as f:
        logging.warning("Loading agent from file")
        agent_json = json.load(f)
        agent = Agent(**agent_json)

else:

    personality = Personality()
    personality.load_traits('traits.json')

    agent_name: str = "Nico"
    agent_definition: str = f"You are {agent_name}, an agent that can experience the virtual world."
    agent = Agent(name="Nico", definition=agent_definition, personality=personality)

url = "https://www.theguardian.com/uk-news/2023/may/04/commonwealth-indigenous-leaders-demand-apology-from-the-king-for-effects-of-colonisation"
readWebsite = ReadWebsite(url=url)
agent.do(readWebsite)

url = "https://www.theguardian.com/world/2023/may/06/sudans-warring-sides-to-begin-talks-in-saudi-arabia-as-fighting-rages-on"
readWebsite = ReadWebsite(url=url, website="theguardian")
agent.do(readWebsite)

reflect = Reflect()
agent.do(reflect)

agent.save("nico.json")

"""
TODO: Specify traits in JSON
"""