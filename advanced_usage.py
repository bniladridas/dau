import random
import sqlite3
from datetime import datetime, timedelta
from src.dau.models.user_activity import UserActivity
from src.dau.tracking.tracker import DAUTracker
from src.dau.reporting.report import DAUReport

class UserSimulator:
    """Simulate user activities for testing and demonstration"""
    PLATFORMS = ['web', 'mobile', 'desktop']
    ACTIVITY_TYPES = [
        'login', 
        'logout', 
        'purchase', 
        'view_product', 
        'add_to_cart', 
        'view_profile', 
        'update_settings'
    ]

    @classmethod
    def generate_activity(cls, user_id=None):
        """Generate a random user activity"""
        return UserActivity(
            user_id=user_id or f'user_{random.randint(1, 100)}',
            timestamp=datetime.now() - timedelta(hours=random.randint(0, 24)),
            activity_type=random.choice(cls.ACTIVITY_TYPES),
            platform=random.choice(cls.PLATFORMS),
            metadata={
                'session_id': f'session_{random.randint(1000, 9999)}',
                'ip_address': f'192.168.{random.randint(0, 255)}.{random.randint(0, 255)}'
            }
        )

def main():
    # Initialize DAU Tracker
    tracker = DAUTracker()
    
    # Simulate generating activities for multiple days
    print("Generating simulated user activities...")
    
    # Generate activities for the past 7 days
    for _ in range(200):  # 200 random activities
        activity = UserSimulator.generate_activity()
        tracker.log_activity(activity)
    
    # Initialize Report Generator
    report = DAUReport()
    
    # Get DAU Trend
    print("\n--- DAU Trend (Last 7 Days) ---")
    dau_trend = report.get_dau_trend(days=7)
    for day in dau_trend:
        print(f"{day['date']}: {day['daily_active_users']} users")
    
    # Get Activity Distribution
    print("\n--- Activity Distribution ---")
    activity_dist = report.get_activity_distribution()
    for activity, users in activity_dist.items():
        print(f"{activity}: {users} unique users")

    # Advanced Reporting: Platform Distribution
    print("\n--- Platform Distribution ---")
    with sqlite3.connect(tracker.db_path) as conn:
        cursor = conn.execute('''
            SELECT platform, COUNT(DISTINCT user_id) as unique_users
            FROM user_activities
            GROUP BY platform
        ''')
        for platform, users in cursor.fetchall():
            print(f"{platform}: {users} unique users")

if __name__ == '__main__':
    main()
