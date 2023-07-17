import requests
import config
from mimesis.agent.agent import Agent


def create_agent(name, definition):
    """"
    Function to create an Agent. Just a wrapper for the API call.
    """
    api_url = f"{config.API_URL}/agents/"
    agent = Agent(name=name, definition=definition)
    agent_json = agent.model_dump(exclude=["LLM"])
    response = requests.post(api_url, json=agent_json)
    return response.json()

def get_agents():
    api_url = f"{config.API_URL}/agents/"
    response = requests.get(api_url)
    return response.json()

def agent_do(agent_id, action_id, action_args: dict):
    api_url = f"{config.API_URL}/agents/{agent_id}/do/{action_id}/"
    response = requests.put(api_url, json=action_args)
    return response.json()