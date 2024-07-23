from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import logging

logger = logging.getLogger(__name__)

def notify_channel_layer(instance, message):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.error('Channel layer is None. WebSocket notifications will not be sent.')
        return

    try:
        nomination_data = {
            'id': instance.id,
            'competition': {
                'id': instance.competition_id.id,
                'competition_name': instance.competition_id.competition_name,
                'competition_city': instance.competition_id.competition_city,
                'competition_date': instance.competition_id.competition_date.isoformat(),
                'competition_qty_days': instance.competition_id.competition_qty_days,
            },
            'nomination_name': instance.nomination_name,
            'nomination_start_date_time': instance.nomination_start_date_time.isoformat(),
            'performance_second': instance.performance_second,
            'delay_between_performance_second': instance.delay_between_performance_second,
        }
        async_to_sync(channel_layer.group_send)(
            'nomination_group_info',
            {
                'type': 'update_message',
                'message': json.dumps({
                    'message': message,
                    'nomination_data': nomination_data
                })
            }
        )
        logger.info(f'Message sent to channel layer: {message}')
    except AttributeError as e:
        logger.error(f'Error sending message to channel layer: {e}')
    except Exception as e:
        logger.error(f'Unexpected error sending message to channel layer: {e}')
