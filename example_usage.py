from src.dau.models.user_activity import UserActivity
from src.dau.tracking.tracker import DAUTracker
from src.dau.reporting.report import DAUReport
from datetime import datetime

def main():
    # Initialize DAU Tracker
    tracker = DAUTracker()

    # Log some sample user activities
    activities = [
        UserActivity(activity_type='login', platform='web'),
        UserActivity(activity_type='purchase', platform='mobile'),
        UserActivity(activity_type='view_content', platform='desktop')
    ]

    for activity in activities:
        tracker.log_activity(activity)

    # Get Daily Active Users
    dau_count = tracker.get_daily_active_user_count()
    print(f"Daily Active Users: {dau_count}")

    # Generate Reports
    report = DAUReport()
    dau_trend = report.get_dau_trend(days=7)
    print("DAU Trend:")
    for day in dau_trend:
        print(f"{day['date']}: {day['daily_active_users']} users")

    activity_dist = report.get_activity_distribution()
    print("\nActivity Distribution:")
    for activity, users in activity_dist.items():
        print(f"{activity}: {users} unique users")

if __name__ == '__main__':
    main()
