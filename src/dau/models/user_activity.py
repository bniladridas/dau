from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class UserActivity:
    user_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    activity_type: str = ''
    platform: str = ''
    metadata: dict = field(default_factory=dict)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'timestamp': self.timestamp.isoformat(),
            'activity_type': self.activity_type,
            'platform': self.platform,
            'metadata': self.metadata
        }
