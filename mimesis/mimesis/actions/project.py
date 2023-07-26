#
import logging
from typing import Literal, Union
from mimesis.actions.actions import Action
from mimesis.agent.agent import Agent
import mimesis.tools as tools
from pydantic import Json

class EvaluatePrompt( Action):
    name: str = "Evaluate prompt"
    description: str = "Considers a prompt and checks if information is enough to create a project"
    definition: str = ""
    project_description: str = ""

    def memory(self, agent: Agent) -> str:
        return f"I checked news headlines"

    def do(self, agent: Agent) ->  str:
        return f"""I have an audio transcription of a person describing a project. The transcription is the following:
    
    {self.project_description}

    From this rough description, I want to generate a document description document. Do you think this is enough information to generate a document description? If no, could you give me advise on how to improve the description so that you can generate an excelent project description?
"""

class WriteProject(Action):
    name: str = "Evaluate prompt"
    description: str = "Considers a prompt and checks if information is enough to create a project"
    definition: str = ""
    project_description: str = ""

    def memory(self, agent: Agent) -> str:
        return f"I checked news headlines"

    def do(self, agent: Agent) ->  str:
        return f"""Consider the following audio transcription describing a project:

=== project description

{self.project_description}

=== end of project description

From this project description, identify the following elements:

1. Project title.

2. Main objectives. Please use the SMART framework to write the objetives: each should be specific, measurable, achievable, relevant and time bound.

3. Project background. This should summarize briefly why the project is necessary and how it will benefit the organization or users.

4. Project timeline. This should include the expected beginning and end dates. If those dates are not found in the context, please identify an estimated lenght in weeks or months.

5. Project stakeholders. Describe briefly how each is one is affected or should be involved in the project.

6. Risks and assumptions. Describe each briefly, list a maximum of 5 risks and assumptions.

I want you to write this response in JSON format. The JSON should have the following general format:

```
{{
    "title": project title,
    "main_objetives": [{{"objective_1":objective 1,"objective_2":objective 2}}],
    "background": project background,
    "timeline": project timeline,
    "stakeholders": project stakeholders,
    "risks_and_assumptions": risks and assumptions
}}
```

Here is an example:

=== project description

Quiero hacer una tienda que venda juguetes para niños

=== end of project description

```
{{
    "title": "Tienda de juguetes",
    "main_objetives": "Not found"
    "background": "Not found",
    "timeline": "Not found",
    "stakeholders": [{{"stakeholder 1":"Owner","stakeholder 2":"Suppliers"}}]
    "risks_and_assumptions": "Not found"
}}
```

Here is another example:

=== project description

Este proyecto se trata de trabajar con una universidad y los alumnos de esa universidad para hacer de manera colaborativa, utilizando la metodología design thinking, un rediseño de las sillas donde ellos se sientan durante sus clases. En la primera etapa del proyecto, que va a durar aproximadamte un mes, vamos a hacer entrevistas a estudiantes, tres focus groups. En base a eso vamos a diseñar una convocatoria. El proceso de convocatoria para que distintos grupos de estudiantes se inscriban para poder participar en el diseño de la silla. Durante los meses siguientes vamos a seleccionar equipos de todas las personas que postularon, los vamos a capacitar en design thinking, vamos a estar acompañando al desarrollo de esos prototipos, y luego vamos a evaluar los diseños que ellos generen para identificar cuáles son los mejores y esos pilotearlos. Finalmente en el mes 6 del proyecto vamos a diseñar el plan de implementación del proyecto finalista.

=== end of project description

```
{{
    "title": "Rediseño de Sillas Universitarias a través de Design Thinking",
    "main_objectives": [
        {{
            "description":"To conduct student interviews and form focus groups within one month to understand their needs and expectations from the university chairs",
            "specific":"True",
            "measurable":"It could have well definite metric, for example, how many student interviews are going to be realized",
            "achievable":"True",
            "relevant":"True",
            "time bound":"True"
        }},
        {{
            "description":"To create a call for entries within the first month where different groups of students can register to participate in the chair design",
            "specific":"True",
            "measurable":"True",
            "achievable":"True",
            "relevant":"True",
            "time bound":"True"
        }},
        {{
            "description":"To select teams from the applicants in the following months, and train them in design thinking",
            "specific":"It would be better to specify how much more following months",
            "measurable":"How many teams are going to be selected?",
            "achievable":"True",
            "relevant":"True",
            "time bound":"True"
        }},
        {{
            "description":"To support the development of chair prototypes and evaluate the designs to identify the best ones for piloting",
            "specific":"True",
            "measurable":"True",
            "achievable":"True",
            "relevant":"True",
            "time bound":"True"
        }},
        {{
            "description":"To design an implementation plan for the final project by the end of the 6th month"
            "specific":"True",
            "measurable":"True",
            "achievable":"True",
            "relevant":"True",
            "time bound":"True"
        }}
    ],
    "background": "This project is necessary as it aims to improve the seating experience for university students during their classes. It seeks to engage students in a collaborative manner by employing the design thinking methodology. The end goal is to create chair designs that are ergonomic, comfortable, and conducive to learning.",
    "timeline": "The project is expected to start immediately with a duration of six months. The initial month is dedicated to gathering insights from students, followed by selection and training of teams in the following months, development and evaluation of prototypes, and finalizing with the design of an implementation plan.",
    "stakeholders": [
        {{
            "name":"University",
            "role":"They will provide resources and support for the project, and benefit from improved student satisfaction and possibly better learning outcomes"
        }},
        {{
            "name":"Students",
            "role":"They will participate in the design process, providing their input, learning from the process, and ultimately being the users of the final product"
        }},
        {{
            "name":"Project team",
            "role":"They will conduct the interviews, guide the design process, and help implement the final design"
        }}
    ],
    "risks_and_assumptions": [
        {{
            "type":"risk",
            "description":"Low participation from students in the design process"
        }},
        {{
            "type":"risk",
            "description": "Delays in project timelines due to unforeseen issues"
        }},
        {{
            "type":"risk",
            "description": "Insufficient resources for prototyping"
        }},
        {{
            "type":"risk",
            "description": "The final design might not meet all students' expectations"
        }},
        {{
            "type":"assumption",
            "description": "There will be sufficient interest from students to participate in the project"
        }},
        {{
            "type":"assumption",
            "description": "The university will provide the necessary support and resources for the project"
        }},
        {{
            "type":"assumption",
            "description": "Design thinking methodology will lead to an effective solution"
        }},
        {{
            "type":"assumption",
            "description": "The new design will lead to an improved student experience"
        }}
    ]
}}
```

This is very important: if you don't find one of these elements in the description given, fill the value with 'Not found'.
"""