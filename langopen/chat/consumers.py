import json
import requests
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        language = text_data_json['language']

        def translateMessage(message):
            url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

            payload = {
                "q": message,
                "target": language,
                "source": "en"
            }
            headers = {
	            "content-type": "application/x-www-form-urlencoded",
	            "Accept-Encoding": "application/gzip",
	            "X-RapidAPI-Key": "4d7a4b548emsheca51641ea28fcap1897bbjsn7daa98afcafb",
	            "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
            }
            response = requests.request("POST", url, data=payload, headers=headers)
            firstInd = response.text.find("translatedText")
            temp = response.text.find(":", firstInd + 1)
            secondInd = response.text.find("}", temp + 1)
            return response.text[temp+2:secondInd-1]
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': translateMessage(message)
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))