import streamlit as st
import requests
import router
import pandas as pd
import typing
from mimesis.agent.agent import Agent
from mimesis.personality.personality import Personality
from mimesis.personality.trait import Trait
from mimesis.model import LLM
from mimesis.role.role import Role
from mimesis.memory.memory import Memory
#import streamlit_pydantic as sp

# Make page wide
st.set_page_config(layout="wide")

st.title("Agente")

tab_create, tab_agents = st.tabs(["Create", "Agents"])

@st.cache_resource
def get_agent():
    return Agent(name="Nico", definition="You are Nico, an agent that can experience the virtual world.")

agent = get_agent()
agent.personality = Personality(traits=[
    Trait(name="Openness", category="Cute", description="You are cute.", self_definition="I am cute."),
    Trait(name="Conscientiousness", category="Smart", description="You are smart.", self_definition="I am smart.")]
    )

with tab_create:

    column_agent, column_prompt = st.columns([1,1])

    with column_agent:

        col1, col2 = st.columns([1,1])
        with col1:
            create = st.button("Create agent")
        with col2:
            update = st.button("Update agent")

        input_agent_name = st.text_input("Agent name", value=agent.name)
        input_agent_definition = st.text_area("Definition", value=agent.definition)

        if create:
            router.create_agent(input_agent_name, input_agent_definition)


        def render_field(ctype, name, value, n=0):
            print("render_field")
            if ctype is str:
                st.text_input(f"{ctype.__name__}/{name}/{n}", value)

        def render_class(cls, instance, i=0):

            st.markdown("".join(["##"]*(i+1))+" "+cls.__name__)

            print("class:",cls)
            print("class:",type(cls))
            print("class:",type("nico"))
            print("instance:",instance, type(instance))

            # Iterates over the fields of the class

            field_n = 0

            for field_name, field_def in cls.model_fields.items():

                field_n += 1

                # Get value of the field
                class_to_render = field_def.annotation
                field_type = typing.get_origin(class_to_render)
                if field_type is None:
                    field_type = class_to_render
                if instance is not None:
                    field_value = getattr(instance, field_name)
                else:
                    field_value = None

                print("\t---")
                print("\tfield_name:", field_name)
                print("\tfield_def:", field_def)
                print("\tfield_value:",field_value)
                print("\tfield_type:",field_type)
                print("\targs:",typing.get_args(class_to_render))

                if field_type is list:

                    print("! FUCK THE LISTS !")
                    f = typing.get_args(class_to_render)[0]
                    
                    if f is None: continue

                    if len(field_value) == 0:

                        if f in [Personality, Trait, Memory, Role, LLM]:
                        
                            render_class(f, None, i+1)

                        else: 

                            render_field(field_type, field_name, "", field_n)

                    else:
                        for ins in field_value:
                            if f is str:
                                render_field(field_type, field_name, field_value, field_n)
                            else:
                                render_class(f, ins, i+1)

                elif field_type in [Personality, Trait, Memory, Role, LLM]:

                    render_class(field_type, getattr(instance, field_name), i+1)

                elif field_type in [typing.Union]:
                    
                    print("! FUCK THE UNIONS !", typing.get_args(class_to_render))
                    f = typing.get_args(class_to_render)[0]
                    render_class(f, getattr(instance, field_name), i+1)

                else:

                    render_field(field_type, field_name, field_value, field_n)
                
                print("\t---")

        render_class(Agent, agent)

        if update:
            agent.name = input_agent_name
            agent.definition = input_agent_definition

    with column_prompt:
        
        st.text_area("Prompt",agent.prompt())

print(agent)
print(agent.personality)
print(agent.personality.traits)

with tab_agents:

    agents = router.get_agents()

    #print([v for k,v in agents.items()])

    agents_df = pd.DataFrame.from_dict(agents, orient="index")

    agents_df_ui = agents_df.copy()
    agents_df_ui["delete"] = False
    agents_df_ui["rating"] = 4

    agents_df_ui = st.data_editor(
        agents_df_ui,
        num_rows="dynamic",
        column_config={
            "rating": st.column_config.NumberColumn(
                "Your rating",
                help="How much do you like this command (1-5)?",
                min_value=1,
                max_value=5,
                step=1,
                format="%d ⭐",
            ),
        })

    if any(agents_df_ui["delete"]):
        agent_to_delete_id = agents_df_ui.loc[lambda x: x["delete"]].iloc[0]["name"]
        router.delete_agent(agent_to_delete_id)

    st.write("Personality")