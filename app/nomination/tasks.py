from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

def notify_channel_layer(instance):
    channel_layer = get_channel_layer()
    data = {
        'message': f'Update for {instance.id}',
        'data': instance
    }
    async_to_sync(channel_layer.group_send)(
        'nomination_group_info',
        {
            'type': 'update_message',
            'message': json.dumps(data)
        }
    )
