from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

import json


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'performance_info'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'get_squads':
            squads = await self.get_squads_data()
            response = {
                'status': 'success',
                'squads_data': squads,
            }
            await self.send(text_data=json.dumps(response))
        # pass

    async def update_message(self, event):
        message = event['message']

        await self.send(text_data=message)

    @database_sync_to_async
    def get_squads_data_sync(self):
        from squad.models import Squad
        squads = Squad.objects.all().order_by('performance_date_time')
        return [
            {
                'nomination_name': squad.nomination_id.nomination_name,
                'squad_name': squad.squad_name,
                'performance_date_time': squad.performance_date_time.isoformat(),
            }
            for squad in squads
        ]

    async def get_squads_data(self):
        return await self.get_squads_data_sync()