# ws_channel/tasks.py

from nomination.models import Nomination
from squad.models import Squad
from ws_channel.notifications import notify_channel_layer

def send_notification(instance, message):
    squads = Squad.objects.all()#.filter(nomination_id=instance.nomination_id)
    squads_data = [
        {
            'nomination_name': squad.nomination_id.nomination_name,
            'squad_name': squad.squad_name,
            'performance_date_time': squad.performance_date_time.strftime('%Y-%m-%d %H:%M'),
        }
        for squad in squads
    ]

    notify_channel_layer(squads_data, message)

