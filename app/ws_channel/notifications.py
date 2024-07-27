# ws_channel/notifications.py

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import logging

logger = logging.getLogger(__name__)

def notify_channel_layer(squads_data, message):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.error('Channel layer is None. WebSocket notifications will not be sent.')
        return

    try:
        async_to_sync(channel_layer.group_send)(
            'performance_info',
            {
                'type': 'update_message',
                'message': json.dumps({
                    'message': message,
                    'squads_data': squads_data
                })
            }
        )
        logger.info(f'Message sent to channel layer: {message}')
    except AttributeError as e:
        logger.error(f'Error sending message to channel layer: {e}')
    except Exception as e:
        logger.error(f'Unexpected error sending message to channel layer: {e}')

def send_notification(instance, message):
    from squad.models import Squad
    squads = Squad.objects.all().order_by('performance_date_time')#filter(nomination_id=instance.nomination_id)
    squads_data = [
        {
            'nomination_name': squad.nomination_id.nomination_name,
            'squad_name': squad.squad_name,
            'performance_date_time': squad.performance_date_time.isoformat(),
        }
        for squad in squads
    ]

    logger.info(f'Sending notification: {message}, Data: {squads_data}')
    notify_channel_layer(squads_data, message)
