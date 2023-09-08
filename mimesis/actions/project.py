#
import logging
from typing import Literal, Union
from mimesis.actions.actions import Action, Chain
from mimesis.agent.agent import Agent
import mimesis.tools as tools
from pydantic import Json

class EvaluatePrompt(Action):
    name: str = "Evaluate prompt"
    description: str = "Considers a prompt and checks if information is enough to create a project"
    definition: str = ""
    project_description: str = ""

    def memory(self, agent: Agent) -> str:
        return f"I checked news headlines"

    def do(self, agent: Agent) ->  str:
        return f"""Consider the following audio transcription of a person describing a project:

=== project description
{self.project_description}
=== end project description

I want you to asses if there is enough information in the audio transcription to generate an excellent project charter. The project charter should contain the following elements:
    
1. Project title.

2. Main objectives. Two to four objectives. Please use the SMART framework to write each objetive. Each objective should be specific, measurable, achievable, relevant and time bound.

3. Project background. This should summarize briefly why the project is necessary and how it will benefit the organization or users.

4. Project timeline. This should include the expected beginning and end dates. If those dates are not found in the context, please identify an estimated lenght in weeks or months.

5. Project stakeholders. Describe briefly how each is one is affected or should be involved in the project.

6. Risks and assumptions. Describe each briefly, list a maximum of 5 risks and assumptions.

I do not want you to provide me the project charter, just assess if there is enough information to generate one.

If there is enough information, then let me know, with a brief assessment.

If there is not enough information to generate an excellent project charter, please write what information is missing in order to generate an excellent project charter. BE VERY STRICT. If there is missing information in any of the points, then say that there is not enough information to generate an excellent project charter. If there are any areas that could be further clarified or expanded upon to improve the quality of the project charter, then say there is not enough information. Is there enough information to generate at least two main objectives? If not, then say there is not enough information. If there is no information provided regarding the risks and assumptions for the project, then say that there is not enough information.

Please provide your reply in the following JSON format:
{{
    "enough_information": true,
    "comments":"comments on how to improve the project description"
}}

Here is an example:
input:
=== project description
Este proyecto se trata de trabajar con una universidad y los alumnos de esa universidad para hacer de manera colaborativa, utilizando la metodología design thinking, un rediseño de las sillas donde ellos se sientan durante sus clases. En la primera etapa del proyecto, que va a durar aproximadamte un mes, vamos a hacer entrevistas a estudiantes, tres focus groups. En base a eso vamos a diseñar una convocatoria. El proceso de convocatoria para que distintos grupos de estudiantes se inscriban para poder participar en el diseño de la silla. Durante los meses siguientes vamos a seleccionar equipos de todas las personas que postularon, los vamos a capacitar en design thinking, vamos a estar acompañando al desarrollo de esos prototipos, y luego vamos a evaluar los diseños que ellos generen para identificar cuáles son los mejores y esos pilotearlos. Finalmente en el mes 6 del proyecto vamos a diseñar el plan de implementación del proyecto finalista.
=== end project description
output:
{{
    "enough_information": true,
    "comments":"Based on the provided audio transcription, there is enough information to generate a project charter."
}}

Here is another example:
input:
=== project description
Quiero crear un videojuego.
== end project description
output:
{{
    "enough_information": false,
    "comments":"Based on the provided audio transcription, there is not enough information to generate a complete project charter. The transcription only includes a single sentence stating the desire to create a video game. To create a comprehensive project charter, additional information is necessary, such as the project scope, deliverables, project team, budget, and any constraints or dependencies.\\To improve the description and gather more information for the project charter, consider asking the person the following questions:\\What is the purpose or objective of the video game? Is it for entertainment or educational purposes?\\Who is the target audience for the video game?\\What are the specific features or functionalities that the video game should have?\\Are there any specific platforms or technologies that should be used?\\Is there a specific timeline or deadline for the project?\\What resources (including budget and personnel) are available for the project?\\By gathering more detailed information through these questions, you will be able to create a more effective and informative project charter."
}}

Here is another example:
input:
=== project description
Este proyecto se tata de implementar OKR's en una empresa de Freight Forwarding tradicional. Lo que queremos es lograr más alineamiento en la empresa, que todos vayan para el mismo lado.
=== end project description
output:
{{
    "enough_information": false,
    "comments":"Based on the provided audio transcription, there is not enough information to generate a project charter. The description of the project is very brief and lacks essential details. To create a comprehensive project charter, additional information is necessary.\\The missing information includes:\\Project title: The audio transcription does not provide a specific project title.\\Main objectives: While the audio mentions the implementation of OKRs to achieve alignment in the company, it does not provide specific SMART objectives.\\Project background: The audio briefly mentions the aim of achieving alignment but fails to provide a detailed explanation of why the project is necessary and how it will benefit the organization or users.\\Project timeline: The audio does not mention the expected beginning and end dates or provide an estimated length in weeks or months.\\Project stakeholders: The audio does not provide any information about the stakeholders or how they will be affected or involved in the project.\\Risks and assumptions: The audio does not mention any risks or assumptions related to the project."
}}
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
    "title": {{"text":"project title"}},
    "main_objectives": [
        {{
            "description":"description",
        }},
        {{
            "description":"description",
        }}],
    "background": {{"text":"project background"}},
    "timeline": {{"text":"project timeline"}},
    "stakeholders": [
        {{
            "name":"stakeholder 1 name",
            "role":"stakeholder 1 role"
        }},
        {{
            "name":"stakeholder 2 name",
            "role":"stakeholder 2 role"
        }}],
    "risks_and_assumptions": [
        {{
            "type":"risk 1",
            "description":"risk 1 description"
        }},
        {{
            "type":"assumption 1",
            "description":"assumption 1 description"
        }}
    ]
}}
```

Here is an example:

=== project description

Quiero hacer una tienda que venda juguetes para niños

=== end of project description

```
{{
    "title": {{"text":"Tienda de juguetes"}},
    "main_objectives": "Not found"
    "background": "Not found",
    "timeline": "Not found",
    "stakeholders": [{{"type":"Owner","role":"Owner of the company"}},{{"type":"Suppliers","role":"Suppliers of the company"}},{{"type":"Customers","role":"Customers of the company"}}]
    "risks_and_assumptions": "Not found"
}}
```

Here is another example:

=== project description

Este proyecto se trata de trabajar con una universidad y los alumnos de esa universidad para hacer de manera colaborativa, utilizando la metodología design thinking, un rediseño de las sillas donde ellos se sientan durante sus clases. En la primera etapa del proyecto, que va a durar aproximadamte un mes, vamos a hacer entrevistas a estudiantes, tres focus groups. En base a eso vamos a diseñar una convocatoria. El proceso de convocatoria para que distintos grupos de estudiantes se inscriban para poder participar en el diseño de la silla. Durante los meses siguientes vamos a seleccionar equipos de todas las personas que postularon, los vamos a capacitar en design thinking, vamos a estar acompañando al desarrollo de esos prototipos, y luego vamos a evaluar los diseños que ellos generen para identificar cuáles son los mejores y esos pilotearlos. Finalmente en el mes 6 del proyecto vamos a diseñar el plan de implementación del proyecto finalista.

=== end of project description

```
{{
    "title": {{
        "text":"Rediseño de Sillas Universitarias a través de Design Thinking"
    }},
    "main_objectives": [
        {{
            "description":"To conduct student interviews and form focus groups within one month to understand their needs and expectations from the university chairs",
        }},
        {{
            "description":"To create a call for entries within the first month where different groups of students can register to participate in the chair design",
        }},
        {{
            "description":"To select teams from the applicants in the following months, and train them in design thinking",
        }},
        {{
            "description":"To support the development of chair prototypes and evaluate the designs to identify the best ones for piloting",
        }},
        {{
            "description":"To design an implementation plan for the final project by the end of the 6th month"
        }}
    ],
    "background": {{
        "text":"This project is necessary as it aims to improve the seating experience for university students during their classes. It seeks to engage students in a collaborative manner by employing the design thinking methodology. The end goal is to create chair designs that are ergonomic, comfortable, and conducive to learning.",
    }},
    "timeline": {{
        "text":"The project is expected to start immediately with a duration of six months. The initial month is dedicated to gathering insights from students, followed by selection and training of teams in the following months, development and evaluation of prototypes, and finalizing with the design of an implementation plan.",
    }},
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

class WriteProjectCharter(Action):
    name: str = "Create a project charter"
    description: str = "Create a project charter"
    definition: str = ""
    project_description: str = ""
    reply_type: str = "document"
    reply_name: str = "project_charter"

    def memory(self, agent: Agent) -> str:
        return f"I checked news headlines"

    def do(self, agent: Agent) ->  str:
        return f"""Act as a senior project manager, with more than 20 years of experience in managing all kinds of projects.
        
Consider the following audio transcription describing a project:

=== project description

{self.project_description}

=== end of project description

From this project description, I want you to write a project charter. Clarity is Key: Be clear and concise. Avoid jargon and ensure that someone without domain knowledge can understand the project's basics. The project charter should include the following elements:

1. Title and Project Name: This might seem basic, but a clear and concise name can help all stakeholders immediately understand the project's main focus.

2. Project Purpose: Define why the project exists. What gap or need is it addressing? How does it align with broader organizational strategies or goals?

3. Project Description:
* Background: Give a brief history of what led to the project initiation.
* Objectives: Clearly outline what the project aims to achieve. Objectives should be SMART (Specific, Measurable, (Achievable, Relevant, and Time-bound).
* Scope: Describe the boundaries. What's in-scope and out-of-scope? This will prevent scope creep later on.

4. Key Stakeholders: Identify who will be involved, who will be affected, and what their roles will be. This can include:

* Project sponsor
* Project manager
* Team members
* End-users
* Any other relevant parties

5. Milestones and Major Deliverables: Break down the major steps, milestones, and deliverables that will mark progress towards the project's completion.

6. Assumptions and Constraints: List the conditions you’re assuming to be true for the project to move forward and any constraints (like time, budget, or resources) that might restrict the project.

7. Risks and Issues: Identify potential pitfalls, challenges, or obstacles and outline strategies or contingencies for managing them.

8. Budget: Highlight the financial resources allocated to the project. Break it down to show where the money is going.

9. Timeline: Establish a high-level timeline for the project, identifying start and end dates, and any critical path items.

10. Success Criteria: Define what will be considered a successful completion of the project. This will be critical for the project's closeout and post-mortem.

11. Communication Plan: State how information will be shared among stakeholders, including frequency, method (meetings, emails, reports), and key contact information.

This is very important, when you don't find specific information in the project description given, use placeholders. For example, if you don't find the project title, write '<Project title>'.

Very important: please provide your answer using Markdown.
"""

class ReviseProject(Action):
    name: str = "Evaluate prompt"
    description: str = "Considers a prompt and checks if information is enough to create a project"
    definition: str = ""
    project_charter: str = ""

    def memory(self, agent: Agent) -> str:
        return f"I checked news headlines"

    def do(self, agent: Agent) ->  str:
        return f"""I want you to revise a project charter. The project charter is in a JSON format, and contains the following elements.
        
1. Project title.

2. Main objectives. Please use the SMART framework to write the objetives: each should be specific, measurable, achievable, relevant and time bound.

3. Project background. This should summarize briefly why the project is necessary and how it will benefit the organization or users.

4. Project timeline. This should include the expected beginning and end dates. If those dates are not found in the context, please identify an estimated lenght in weeks or months.

5. Project stakeholders. Describe briefly how each is one is affected or should be involved in the project.

6. Risks and assumptions. Describe each briefly, list a maximum of 5 risks and assumptions.

Here is the project charter, delimited by three equal signs.

=== project charter

{self.project_charter}"

=== end of project charter

Please provide either questions or insights in each section that would help me further enhance the project. Return your response in JSON format, with the previous structure, adding a variable "comments" to each element with your comments on it. Do not reply with anything else than the JSON.

Here is an example:

=== project charter

{{
    "title": {{
        "text":"Rediseño de Sillas Universitarias a través de Design Thinking"
    }},
    "main_objectives": [
        {{
            "description":"To conduct student interviews and form focus groups within one month to understand their needs and expectations from the university chairs",
        }},
        {{
            "description":"To create a call for entries within the first month where different groups of students can register to participate in the chair design",
        }},
        {{
            "description":"To select teams from the applicants in the following months, and train them in design thinking",
        }},
        {{
            "description":"To support the development of chair prototypes and evaluate the designs to identify the best ones for piloting",
        }},
        {{
            "description":"To design an implementation plan for the final project by the end of the 6th month"
        }}
    ],
    "background": {{
        "text":"This project is necessary as it aims to improve the seating experience for university students during their classes. It seeks to engage students in a collaborative manner by employing the design thinking methodology. The end goal is to create chair designs that are ergonomic, comfortable, and conducive to learning.",
    }},
    "timeline": {{
        "text":"The project is expected to start immediately with a duration of six months. The initial month is dedicated to gathering insights from students, followed by selection and training of teams in the following months, development and evaluation of prototypes, and finalizing with the design of an implementation plan.",
    }},
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

=== end of project charter

{{
    "title": {{
        "text":"Rediseño de Sillas Universitarias a través de Design Thinking",
        "comments":"The project title, "Rediseño de Sillas Universitarias a través de Design Thinking," is clear and descriptive. However, it could be enhanced by adding a specific identifier for the university involved. For example, "Rediseño de Sillas de la Universidad XYZ a través de Design Thinking." This modification will make it more tailored to the actual institution and eliminate any ambiguity about the university's identity."
    }},
    "main_objectives": [
        {{
            "description":"To conduct student interviews and form focus groups within one month to understand their needs and expectations from the university chairs",
            "comments":""
        }},
        {{
            "description":"To create a call for entries within the first month where different groups of students can register to participate in the chair design",
            "comments":""
        }},
        {{
            "description":"To select teams from the applicants in the following months, and train them in design thinking",
            "comments":"Consider specifying the exact number of following months and the number of teams to be selected for more clarity."
        }},
        {{
            "description":"To support the development of chair prototypes and evaluate the designs to identify the best ones for piloting",
            "comments":""
        }},
        {{
            "description":"To design an implementation plan for the final project by the end of the 6th month",
            "comments":""
        }}
    ],
    "background": {{
        "text":"This project is necessary as it aims to improve the seating experience for university students during their classes. It seeks to engage students in a collaborative manner by employing the design thinking methodology. The end goal is to create chair designs that are ergonomic, comfortable, and conducive to learning.",
        "comments":"The project background succinctly explains the purpose of the project, but it lacks some key details. To improve this section, include relevant statistics or anecdotes highlighting the current issues with the existing chairs, such as discomfort complaints or health concerns from students. Additionally, provide insights into how the redesign aligns with the university's broader strategic goals, emphasizing the impact on the learning experience and student success."
    }},
    "timeline": {{
        "text":"The project is expected to start immediately with a duration of six months. The initial month is dedicated to gathering insights from students, followed by selection and training of teams in the following months, development and evaluation of prototypes, and finalizing with the design of an implementation plan.",
        "comments":"The provided timeline outlines the project's major stages, but it lacks specific dates or durations. To enhance clarity, include actual start and end dates for each stage, ensuring a well-defined schedule. Additionally, consider breaking down the timeline into more granular milestones and their associated deadlines to facilitate project tracking and progress monitoring."
    }},
    "stakeholders": [
        {{
            "name":"University",
            "role":"They will provide resources and support for the project, and benefit from improved student satisfaction and possibly better learning outcomes",
            "comments":""
        }},
        {{
            "name":"Students",
            "role":"They will participate in the design process, providing their input, learning from the process, and ultimately being the users of the final product",
            "comments":""
        }},
        {{
            "name":"Project team",
            "role":"They will conduct the interviews, guide the design process, and help implement the final design",
            "comments":""
        }}
    ],
    "risks_and_assumptions": [
        {{
            "type":"risk",
            "description":"Low participation from students in the design process",
            "comments":""
        }},
        {{
            "type":"risk",
            "description": "Delays in project timelines due to unforeseen issues",
            "comments":""
        }},
        {{
            "type":"risk",
            "description": "Insufficient resources for prototyping",
            "comments":""
        }},
        {{
            "type":"risk",
            "description": "The final design might not meet all students' expectations",
            "comments":""
        }},
        {{
            "type":"assumption",
            "description": "There will be sufficient interest from students to participate in the project",
            "comments":""
        }},
        {{
            "type":"assumption",
            "description": "The university will provide the necessary support and resources for the project",
            "comments":""
        }},
        {{
            "type":"assumption",
            "description": "Design thinking methodology will lead to an effective solution",
            "comments":""
        }},
        {{
            "type":"assumption",
            "description": "The new design will lead to an improved student experience",
            "comments":""
        }}
    ]
}}
"""

class ReviseProjectCharter(Action):
    name: str = "Evaluate prompt"
    description: str = "Considers a prompt and checks if information is enough to create a project"
    definition: str = ""
    project_charter: str = ""
    reply_type: str = "message"
    reply_name: str = "project_charter"

    def memory(self, agent: Agent) -> str:
        return f"I checked news headlines"

    def do(self, agent: Agent) ->  str:
        return f"""Act as a senior project manager, with more than 20 years of experience in managing all kinds of projects. 

I want you to revise a project charter. Please provide either questions or insights in each section that would help further enhance the project. For example, you could ask for more details about the project's timeline or stakeholders. You could also provide insights about the project's risks and assumptions, or suggest ways to improve the project's objectives. In every item you could ask for more information to make this project charter more informative and useful. Be imaginative and creative. If you have no suggestions in a section, it is not necessary to indicate it.

Include suggestions on what could be missing in each section.

Please DO NOT include the content of the project charter, just the comments and insights on each section.
        
Here is the project charter, delimited by three equal signs.

=== project charter

{self.project_charter}"

=== end of project charter

Very important: please provide your answer using Markdown.

Super important: DO NOT include the content of the project charter, just the comments and insights on each section.

Here is a template for the output:

## 1. Title and Project Name
*Insights*:

*Questions*:

## 2. Project Purpose
*Insights*:

*Questions*:

## 3. Project Description
*Insights*:

*Questions*:

### Background
*Insights*:

*Questions*:

### Objectives
*Insights*:

*Questions*:

### Scope
*Insights*:

*Questions*:

## 4. Key Stakeholders
*Insights*:

*Questions*:

## 5. Milestones and Major Deliverables
*Insights*:

*Questions*:

## 6. Assumptions and Constraint
### Assumptions
*Insights*:

*Questions*:

### Constraints
*Insights*:

*Questions*:

## 7. Risks and Issues
*Insights*:

*Questions*:

## 8. Budget
*Insights*:

*Questions*:

## 9. Timeline
*Insights*:

*Questions*:

## 10. Success Criteria
*Insights*:

*Questions*:

## 11. Communication Plan
*Insights*:

*Questions*:
"""

class ApplyRevision(Action):
    name: str = "Evaluate prompt"
    description: str = "Considers a prompt and checks if information is enough to create a project"
    definition: str = ""
    project_charter: str = ""

    def memory(self, agent: Agent) -> str:
        return f"I checked news headlines"

    def do(self, agent: Agent) ->  str:
        return f"""I have a project charter with revisions from a top project manager. The project charter has the following elements.
        
1. Project title.

2. Main objectives. Please use the SMART framework to write the objetives: each should be specific, measurable, achievable, relevant and time bound.

3. Project background. This should summarize briefly why the project is necessary and how it will benefit the organization or users.

4. Project timeline. This should include the expected beginning and end dates. If those dates are not found in the context, please identify an estimated lenght in weeks or months.

5. Project stakeholders. Describe briefly how each is one is affected or should be involved in the project.

6. Risks and assumptions. Describe each briefly, list a maximum of 5 risks and assumptions.

It is written in the following JSON format.

{{
    "title": {{"text":"project title","comments":"comments done by project manager regarding the title"}},
    "main_objectives": [
        {{
            "description":"description",
            "comments":"comments done by project manager regarding the first objective"
        }},
        {{
            "description":"description",
            "comments":"comments done by project manager regarding the second objective"
        }}],
    "background": {{"text":"project background","comments":"comments done by project manager regarding the background"}},
    "timeline": {{"text":"project timeline","comments":"comments done by project manager regarding the timeline"}},
    "stakeholders": [
        {{
            "name":"stakeholder 1 name",
            "role":"stakeholder 1 role",
            "comments":"comments done by the project manager regarding the first stakeholder"
        }},
        {{
            "name":"stakeholder 2 name",
            "role":"stakeholder 2 role",
            "comments":"comments done by the project manager regarding the second stakeholder"
        }}],
    "risks_and_assumptions": [
        {{
            "type":"risk 1",
            "description":"risk 1 description",
            "comments":"comments done by the project manager regarding the first risk"
        }},
        {{
            "type":"assumption 1",
            "description":"assumption 1 description",
            "comments":"comments done by the project manager regarding the second risk"
        }}
    ]
}}

I want you to rewrite the project charter applying the comments done by the project manager in each element. If there are no comments just leave the element as it is. If you have no information to apply the comments, then just make it up. 

For example, consider the following element:

== Original element

{{
"main_objectives": [
    {{
        "description":"To select teams from the applicants in the following months, and train them in design thinking",
        "comments":"Main objective is specific, measurable, achievable, relevant, and time-bound. Consider specifying the exact number of following months and the number of teams to be selected for more clarity."
    }}]
}}

== Revised element

{{
    "main_objectives": [
    {{
        "description":"To select teams from the applicants in the two following months, and train them in design thinking. There will be 5 teams in total."
    }}]
}}

==

Here is another example for another element:

== Original element

"stakeholders":
{{
    "description":"Not found",
    "comments":"The timeline for the project is not specified in the provided project charter. It is crucial to establish clear timelines and deadlines for each phase of the project to ensure timely completion. Please provide more information regarding the expected beginning and end dates or the estimated duration in weeks or months."
}}

== Revised element

"stakeholders":
{{
    "description":"The project will be conducted in the following two quarters: from January to June 2023. The first quarter will be dedicated to the design process, and the second quarter will be dedicated to the implementation process. In the first quarter, the first month will be dedicated to train each team in OKR's. The second month and third month will be dedicated to define the first objectives and key results, first of the c-level, and then for each team.",
}}

==

Here is the project charter:

{self.project_charter}
"""
        
class ApplyRevisionCharter(Action):
    name: str = "Evaluate prompt"
    description: str = "Considers a prompt and checks if information is enough to create a project"
    definition: str = ""
    project_charter: str = ""
    project_revisions: str = ""

    def memory(self, agent: Agent) -> str:
        return f"I checked news headlines"

    def do(self, agent: Agent) ->  str:
        reply = f"""Act as a senior project manager, with more than 20 years of experience in managing all kinds of projects. 
        
I want you to rewrite a project charter applying the comments done by a senior executive in each element. I will first give you the project charter in its current version, and then a list of comments for each section. If you have no information to fullfill the comments, make it up, or use placeholders.

Very important: modify the project charter so that ALL COMMENTS ARE CONSIDERED. DO NOT INCLUDE THE COMMENTS OR INSIGHTS IN THE REVISED PROJECT CHARTER.

Very important: please provide your answer using Markdown.

Both the project charter and the revisions follow, delimited by three equal signs. 

=== Project charter
{self.project_charter}

=== Project revisions
{self.project_revisions}
"""
        print(reply)
        return reply
    
class WriteAndReviseProjectCharter(Chain):

    params: dict = {}

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)
        self.params = kwargs
        self.add_action(WriteProjectCharter)
        self.add_action(ReviseProjectCharter)

    def get_action(self, index, previous_reply):
        if previous_reply:
            reply_dict = {previous_reply["name"]:previous_reply["text"]}
            action = self.actions[index](**reply_dict)
        else:
            action = self.actions[index](**self.params)
        return action