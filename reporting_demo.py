from src.dau.models.user_activity import UserActivity
from src.dau.tracking.tracker import DAUTracker
from src.dau.reporting.report import DAUReport
import random
from datetime import datetime, timedelta

def generate_sample_data(tracker, num_activities=500):
    """Generate sample user activities for reporting demonstration"""
    platforms = ['web', 'mobile', 'desktop']
    activity_types = ['login', 'purchase', 'view_product', 'add_to_cart', 'update_profile', 'share_content']
    
    for _ in range(num_activities):
        # Simulate activities spread across different dates and with varied timestamps
        activity_date = datetime.now() - timedelta(days=random.randint(0, 30))
        
        activity = UserActivity(
            timestamp=activity_date,
            activity_type=random.choice(activity_types),
            platform=random.choice(platforms),
            metadata={
                'session_duration': random.randint(10, 300),
                'device': random.choice(['chrome', 'firefox', 'safari', 'edge', 'mobile_app']),
                'region': random.choice(['US', 'EU', 'APAC', 'LATAM'])
            }
        )
        
        tracker.log_activity(activity)

def main():
    # Initialize tracker and generate sample data
    tracker = DAUTracker()
    generate_sample_data(tracker)
    
    # Initialize report generator
    report = DAUReport()
    
    # Generate comprehensive report
    print("🔍 Generating Comprehensive DAU Report...")
    comprehensive_report = report.generate_comprehensive_report()
    
    # Print DAU Trend
    print("\n📊 DAU Trend:")
    for day in comprehensive_report['dau_trend']:
        print(f"{day['date']}: {day['daily_active_users']} users")
    
    # Print Activity Distribution
    print("\n🚀 Activity Distribution:")
    for activity, stats in comprehensive_report['activity_distribution'].items():
        print(f"{activity}: {stats['unique_users']} unique users, {stats['total_activities']} total activities")
    
    # Print Platform Performance
    print("\n💻 Platform Performance:")
    for platform, performance in comprehensive_report['platform_performance'].items():
        print(f"{platform}: {performance['unique_users']} unique users, {performance['total_activities']} total activities, Avg Metadata Size: {performance['avg_metadata_size']:.2f}")
    
    # Export DAU Trend to CSV
    print("\n💾 Exporting DAU Trend to CSV...")
    report.export_csv(comprehensive_report['dau_trend'], 'dau_trend.csv')
    
    print(f"\n📁 Reports and exports are available in the 'reports' directory.")

if __name__ == '__main__':
    main()
