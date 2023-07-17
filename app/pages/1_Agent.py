import streamlit as st
import requests
import router
import pandas as pd

st.title("Agente")

tab_create, tab_agents = st.tabs(["Create", "Agents"])

with tab_create:

    agent_name: str = "Nico"
    agent_definition: str = f"You are {agent_name}, an agent that can experience the virtual world."

    input_agent_name = st.text_input("Agent name", value=agent_name)
    input_agent_definition = st.text_area("Definition", value=agent_definition)

    create = st.button("Create agent")
    
    if create:
        router.create_agent(input_agent_name, input_agent_definition)

with tab_agents:

    agents = router.get_agents()

    #print([v for k,v in agents.items()])

    agents_df = pd.DataFrame.from_dict(agents, orient="index")

    st.table(agents_df)