import streamlit as st
import tools
import router

st.title("Wise App")

# Get data
agents = router.get_agents()

# Agent selector
agent = st.selectbox("Agent", options=[k["name"] for v,k in agents.items()])#, format_func=lambda x: agents[x]["name"])

prompt = st.chat_input("Prompt")

if prompt:
    st.write(f"Me: {prompt}")
    answer = router.agent_do(agent, "answer", {"prompt":prompt})
    st.write(f"{agent}: {answer}")