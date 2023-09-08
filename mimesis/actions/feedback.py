#
import logging
from typing import Literal, Union
from mimesis.actions.actions import Action
from mimesis.agent.agent import Agent
import mimesis.tools as tools
from pydantic import Json

class FeedbackGuidelines(Action):
    name: str = "Guidelines for proper feedback"
    description: str = ""
    definition: str = ""
    reply_type: str = "document"
    reply_name: str = "feedback_guidelines"
    situation: str = ""

    def memory(self, agent: Agent) -> str:
        return f"I gave feedback"

    def do(self, agent: Agent) ->  str:
        prompt = f"""The SBI (Situation-Behavior-Impact) framework is a structured method for providing specific, clear, and meaningful feedback. Here's a short description of each component:

Situation: Begin by describing the specific situation where the behavior occurred. It's important to ground your feedback in a real, tangible event or moment to provide context. For example, "During our team meeting yesterday..."

Behavior: Then, articulate the behavior you observed. The behavior should be an objective description of what the person did, without attaching any interpretations or value judgments. For example, "I noticed that you interrupted others while they were speaking..."

Impact: Finally, explain the impact that this behavior had. The impact can be on you, the team, the project, or any other relevant stakeholder. It's essential to focus on how the behavior affected the situation, not on the person’s intentions. For example, "This made some team members feel unheard and may have prevented us from hearing valuable insights."

This framework can be used for giving both positive and constructive feedback. The key is to be as specific and factual as possible, and focus on observable behaviors, not on assumed intentions.

You are a Senior Coach. Your are tasked with providing me clear guidelines and tips to give proper feedback to a colleague or worker.

Now, consider the following situation as context: 

“{self.situation}”

First identify if the above context describes a positive situation that should be reinforced and scaled, or a negative situation that should be avoided or mitigated.

Then elaborate and provide guidelines to hold a feedback meeting using the SBI framework. Please provide specific recommendations (including how to behave and what to say) and suggested topics of conversation, always considering specific elements of the situation given as context. Please provide the answer in the markdown format.
"""
        return prompt
    
class FeedbackValues(Action):
    name: str = "Align feedback with company values"
    description: str = ""
    definition: str = ""
    feedback: str = ""

    def memory(self, agent: Agent) -> str:
        return f"I gave feedback"

    def do(self, agent: Agent) ->  str:
        prompt = f"""Consider the following guideline to give criticism:

{self.feedback}
        
Now, please update the guidelines and recommendations considering the culture the company wants to develop. The new and recommendation should serve to also communicate the company values and reinforce expected conducts. Here are the company values:

“1.	Creatividad (Creativity):

Description: Creemos en el poder transformador de la creatividad. Ella nos lleva más allá de lo ordinario, hacia soluciones innovadoras y emocionantes. La creatividad es nuestra herramienta para enfrentar desafíos y explorar nuevas posibilidades.

Expected behaviors:

	•	Propone soluciones innovadoras para desafíos complejos.
	•	Abierto a nuevas ideas y perspectivas.
	•	Busca constantemente aprender y explorar más allá de su propia zona de confort.
	•	Se permite tomar riesgos y aprender de los errores.

	2.	Método (Method):

Description: Comprendemos que la creatividad florece en un marco de rigurosidad y estructura. Nos enfocamos en la excelencia de nuestro método, estableciendo procesos claros y estructurados que permiten el flujo efectivo de ideas.

Expected behaviors:

	•	Cumple con las políticas, procedimientos y estándares establecidos.
	•	Constantemente busca mejorar y optimizar procesos.
	•	Valora y se adapta a los cambios en las estrategias y metodologías de trabajo.
	•	Emplea un enfoque sistemático para resolver problemas.

	3.	Excelencia (Excellence):

Description: Nos esforzamos por la excelencia en todo lo que hacemos, buscando siempre superar nuestras propias expectativas. La excelencia para nosotros significa ir un paso más allá, sin dejar de disfrutar el viaje.

Expected behaviors:

	•	Produce trabajo de alta calidad.
	•	Busca constantemente maneras de mejorar.
	•	Acepta y se nutre de la retroalimentación.
	•	Toma la iniciativa y asume la responsabilidad de sus acciones.

	4.	Respeto (Respect):

Description: Valoramos y respetamos a cada individuo, reconociendo la diversidad como fuente de fortaleza. Entendemos que cada persona tiene su propia perspectiva única, que contribuye a la riqueza de nuestras ideas y al crecimiento de nuestra organización.

Expected behaviors:

	•	Escucha y valora las opiniones y puntos de vista de los demás.
	•	Se comporta de manera ética y trata a los demás con dignidad y consideración.
	•	Promueve un ambiente inclusivo y libre de discriminación.
	•	Resuelve los conflictos de manera constructiva y profesional.

	5.	Transparencia (Transparency):

Description: Creemos en la transparencia como pilar de la confianza y el trabajo en equipo. La comunicación abierta y honesta nos permite trabajar de manera efectiva y construir relaciones sólidas.

Expected behaviors:

	•	Comparte información de manera clara y oportuna.
	•	Es honesto y directo, manteniendo la sensibilidad hacia los demás.
	•	Asume la responsabilidad de sus acciones y decisiones.
	•	Fomenta un ambiente de confianza al actuar con integridad y consistencia.”

Please underline the company values in the proposed feedback. Do not give me the old advise on feedback, just the new updated one.

This is very important: please provide your answer in Markdown format. 
"""
        print(prompt)
        return prompt