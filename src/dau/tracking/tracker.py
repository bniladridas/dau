import sqlite3
from datetime import datetime, timedelta
from typing import List, Optional
from ..models.user_activity import UserActivity

class DAUTracker:
    def __init__(self, db_path: str = 'dau_tracking.db'):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_activities (
                    user_id TEXT,
                    timestamp TEXT,
                    activity_type TEXT,
                    platform TEXT,
                    metadata TEXT
                )
            ''')

    def log_activity(self, activity: UserActivity):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO user_activities 
                (user_id, timestamp, activity_type, platform, metadata) 
                VALUES (?, ?, ?, ?, ?)
            ''', (
                activity.user_id, 
                activity.timestamp.isoformat(), 
                activity.activity_type, 
                activity.platform, 
                str(activity.metadata)
            ))

    def get_daily_active_users(self, date: Optional[datetime] = None) -> List[str]:
        if date is None:
            date = datetime.now()
        
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT DISTINCT user_id 
                FROM user_activities 
                WHERE timestamp >= ? AND timestamp < ?
            ''', (start_of_day.isoformat(), end_of_day.isoformat()))
            
            return [row[0] for row in cursor.fetchall()]

    def get_daily_active_user_count(self, date: Optional[datetime] = None) -> int:
        return len(self.get_daily_active_users(date))
