import json
import openai
import pypandoc
import logging
from datetime import datetime

from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
# Import OPENAI_API_KEY from settings.py
from django.conf import settings

from document.models import Document

openai.api_key = settings.OPENAI_API_KEY

class OpenAIConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        logging.warning("OpenAIConsumer.connect " + self.channel_name)
        # We set the group_name to the url of the view (with parameters),
        # so that then we can send the message to the correct group from the view.
        # If no name is given default to global.
        params = parse_qs(self.scope["query_string"].decode("utf-8"))
        if "group_name" in params.keys():
            group_name = params["group_name"][0].replace("/", "")
        else:
            group_name = "openai_group"
        await self.channel_layer.group_add(group_name, self.channel_name)
        self.groups.append(group_name) # important otherwise some cleanup does not happened on disconnect.
        await self.accept()

    async def receive(self, text_data):
        print("OpenAIConsumer.receive")
        
        # Assuming you're sending a prompt from the client
        data = json.loads(text_data)
        prompt = data['prompt']

        response_stream = await openai.ChatCompletion.acreate(model='gpt-4',
        #response_stream = await openai.ChatCompletion.acreate(model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.5,
            stream=True)
        
        response_text = ""
        
        async for r in response_stream:
            if r.choices[0].delta == {}:
                # Convert markdown to document formatted (editor.js) json
                document_json = Document.markdown_to_json(response_text)
                await self.send(text_data=json.dumps({'status': 'end', 'document_json': document_json}))
                break
            else:
                response_text += r.choices[0].delta.content
                document_json = Document.markdown_to_json(response_text)
                await self.send(text_data=json.dumps({
                    'status': 'continue',
                    'response': r.choices[0].delta.content,
                    'document_json': document_json
                }))

    async def llm_call(self, event):
        print("OpenAIConsumer.llm_call")

        fast = event.get('fast', False)

        # Call ChatCompletion API
        #response_stream = await openai.ChatCompletion.acreate(model='gpt-3.5-turbo',
        response_stream = await openai.ChatCompletion.acreate(model='gpt-4',
            messages=[
                {'role': 'user', 'content': event['prompt']}
            ],
            temperature=0.5,
            stream=True)
        
        response_text = ""

        # Get initial current time
        current_time = datetime.now()
        
        async for response in response_stream:
            # Stream of chunks of text, contained in choices[0].delta.
            # If delta is empty, then it's the last one, send status end to front
            if response.choices[0].delta == {}:
                
                with open("response.txt", "w") as text_file:
                    text_file.write(response_text)
                
                pypandoc_json = pypandoc.convert_text(response_text, 'json', format='md')
                with open("json.txt", "w") as text_file:
                    text_file.write(pypandoc_json)

                document_json = Document.markdown_to_json(response_text)
                print(json.dumps(document_json))
                with open("editor_json.txt", "w") as text_file:
                    text_file.write(json.dumps(document_json))
                    
                await self.send(text_data=json.dumps({
                    'status': 'end',
                    'response_text': response_text,
                    'document_json': document_json
                    }))
                break
            else:
                # Send chunk to front
                response_text += response.choices[0].delta.content
                # Check if more than a second has ellapsed
                if (datetime.now() - current_time).seconds > 1 or fast:
                    # Convert markdown to document formatted (editor.js) json
                    document_json = Document.markdown_to_json(response_text)
                    await self.send(text_data=json.dumps({
                        'status': 'continue',
                        'response': response.choices[0].delta.content,
                        'response_text': response_text,
                        'document_json': document_json
                        }))
                    # Reset current time
                    current_time = datetime.now()

    async def disconnect(self, event):
        print("disconnect")
        pass