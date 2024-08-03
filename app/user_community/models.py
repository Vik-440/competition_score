"""Model for crossing Users and Communities"""

from django.db.models import (
    Model,
    ForeignKey,
    CASCADE,
)

from community.models import Community
from core.models import User

class UserCommunity(Model):
    """mtm model for users and community"""

    user_id = ForeignKey(User, on_delete=CASCADE, null=False)
    community_id = ForeignKey(Community, on_delete=CASCADE, null=False)

    def __str__(self):
        return f'"user_id" = {self.user_id}, "community_id" = {self.community_id}'
    
    class Meta:
        unique_together = ('user_id', 'community_id')
