from src.dau.learning.predictor import SimpleDAUPredictor
from src.dau.models.user_activity import UserActivity
from src.dau.tracking.tracker import DAUTracker
import random
from datetime import datetime, timedelta

def generate_sample_data(tracker, num_activities=500, data_scenario='default'):
    """
    Generate sample user activities with different data characteristics
    
    Data Scenarios:
    1. 'default': Moderate variability, balanced distribution
    2. 'high_variance': Large fluctuations in user activity
    3. 'consistent': Very stable, predictable user behavior
    4. 'sparse': Limited historical data points
    """
    platforms = ['web', 'mobile', 'desktop']
    activity_types = ['login', 'purchase', 'view_product', 'add_to_cart', 'update_profile']
    
    # Base seed for reproducibility
    random.seed(42)
    
    # Scenario-based data generation
    if data_scenario == 'default':
        # Moderate variability
        base_activities = num_activities
        variance_factor = 0.3
    elif data_scenario == 'high_variance':
        # Large activity fluctuations
        base_activities = num_activities
        variance_factor = 0.7
    elif data_scenario == 'consistent':
        # Very stable behavior
        base_activities = num_activities
        variance_factor = 0.1
    elif data_scenario == 'sparse':
        # Limited data points
        base_activities = num_activities // 4
        variance_factor = 0.2
    else:
        raise ValueError("Invalid data scenario")
    
    for _ in range(base_activities):
        # Simulate activities spread across different dates
        activity_date = datetime.now() - timedelta(days=random.randint(0, 30))
        
        # Variance in activity generation based on scenario
        if data_scenario == 'high_variance':
            # More random, less predictable
            activity_multiplier = random.uniform(0.5, 1.5)
        elif data_scenario == 'consistent':
            # Very stable, close to mean
            activity_multiplier = random.uniform(0.9, 1.1)
        elif data_scenario == 'sparse':
            # Fewer activities, more spread out
            activity_multiplier = random.uniform(0.7, 1.3)
        else:
            # Default moderate variability
            activity_multiplier = random.uniform(0.8, 1.2)
        
        activity = UserActivity(
            timestamp=activity_date,
            activity_type=random.choice(activity_types),
            platform=random.choice(platforms),
            metadata={
                'session_duration': int(random.randint(10, 300) * activity_multiplier),
                'device': random.choice(['chrome', 'firefox', 'safari', 'edge', 'mobile_app']),
                'region': random.choice(['US', 'EU', 'APAC', 'LATAM'])
            }
        )
        
        tracker.log_activity(activity)

def main():
    # Demonstrate different data scenarios
    scenarios = ['default', 'high_variance', 'consistent', 'sparse']
    
    for scenario in scenarios:
        print(f"\n🔍 Scenario: {scenario.replace('_', ' ').title()}")
        
        # Reset tracker for each scenario
        tracker = DAUTracker()
        generate_sample_data(tracker, data_scenario=scenario)
        
        # Initialize predictor
        predictor = SimpleDAUPredictor()
        
        # Predict DAU for next week
        print("🔮 DAU Predictions:")
        predictions = predictor.predict_dau()
        for pred in predictions:
            print(f"{pred['date']}: {pred['predicted_dau']} users")
            print(f"  Confidence: {pred['confidence_level']} (Score: {pred['confidence_score']})")
            print(f"  Details: Avg DAU = {pred['prediction_details']['avg_dau']}, "
                  f"Day Mean = {pred['prediction_details']['day_of_week_mean']}, "
                  f"Day Std = {pred['prediction_details']['day_of_week_std']}\n")
    
    # Analyze User Segments
    print("\n User Segment Analysis:")
    segments = predictor.analyze_user_segments()
    print("Total Users:", segments['total_users'])
    print("\nUser Segments:")
    for segment, percentage in segments['segment_percentages'].items():
        print(f"{segment.replace('_', ' ').title()}: {percentage:.2f}%")

if __name__ == '__main__':
    main()
