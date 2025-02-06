#!/bin/bash

# DAU Tracking System - Data Science Workflow Script
# Simulates a professional data science approach to user activity analysis

# Color codes for better output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# Error handling function
error_exit() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    exit 1
}

# Check if a Python package is installed
is_package_installed() {
    python3 -c "import $1" &> /dev/null
}

# Validate Python environment
validate_environment() {
    log "🔍 Checking Python Environment"
    python3 --version || error_exit "Python3 not installed"
    pip3 --version || error_exit "pip3 not installed"
}

# Data Generation and Preprocessing
prepare_data() {
    log "🗂️ Preparing User Activity Data"
    
    # Generate multiple datasets with different characteristics
    log "   Generating Default Dataset"
    python3 -c "
from src.dau.tracking.tracker import DAUTracker
from src.dau.models.user_activity import UserActivity
import random
from datetime import datetime, timedelta

def generate_dataset(scenario='default', num_activities=1000):
    tracker = DAUTracker(db_path=f'dau_tracking_{scenario}.db')
    
    platforms = ['web', 'mobile', 'desktop']
    activity_types = ['login', 'purchase', 'view_product', 'add_to_cart', 'update_profile']
    
    for _ in range(num_activities):
        activity_date = datetime.now() - timedelta(days=random.randint(0, 90))
        
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

# Generate multiple datasets
generate_dataset('default')
generate_dataset('high_variance')
generate_dataset('consistent')
generate_dataset('sparse')
    "
}

# Exploratory Data Analysis
analyze_data() {
    log "📊 Performing Exploratory Data Analysis"
    
    # Run reporting demo to get comprehensive insights
    python3 -m reporting_demo
    
    # Generate advanced visualizations
    log "   Creating Confidence Visualization"
    python3 -m confidence_visualization
    
    # Optional: If matplotlib is available, create more advanced plots
    python3 -c "
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime, timedelta

def create_advanced_plots():
    conn = sqlite3.connect('dau_tracking_default.db')
    
    # Platform Activity Comparison
    plt.figure(figsize=(12, 5))
    
    platforms = ['web', 'mobile', 'desktop']
    platform_activities = {}
    
    for platform in platforms:
        cursor = conn.execute('''
            SELECT 
                date(timestamp) as activity_date, 
                COUNT(*) as total_activities
            FROM user_activities
            WHERE platform = ?
            GROUP BY activity_date
            ORDER BY activity_date
        ''', (platform,))
        
        platform_activities[platform] = cursor.fetchall()
    
    plt.subplot(1, 2, 1)
    for platform, activities in platform_activities.items():
        dates = [datetime.strptime(row[0], '%Y-%m-%d') for row in activities]
        counts = [row[1] for row in activities]
        plt.plot(dates, counts, label=platform)
    
    plt.title('Platform Activity Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Activities')
    plt.legend()
    
    # Activity Type Distribution
    plt.subplot(1, 2, 2)
    cursor = conn.execute('''
        SELECT 
            activity_type, 
            COUNT(*) as total_activities
        FROM user_activities
        GROUP BY activity_type
    ''')
    
    activity_types = cursor.fetchall()
    plt.pie(
        [row[1] for row in activity_types], 
        labels=[row[0] for row in activity_types], 
        autopct='%1.1f%%'
    )
    plt.title('Activity Type Distribution')
    
    plt.tight_layout()
    plt.savefig('dau_advanced_analysis.png')
    plt.close()

create_advanced_plots()
    "
}

# Machine Learning Predictions
ml_predictions() {
    log "🤖 Machine Learning Predictions"
    
    # Run learning demo with various scenarios
    python3 -m learning_demo
    
    # Check for ML dependencies
    if is_package_installed sklearn && is_package_installed pandas && is_package_installed numpy; then
        log "   Running Advanced ML Predictions"
        python3 -c "
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import sqlite3
import pandas as pd

def advanced_ml_prediction():
    # Connect to database
    conn = sqlite3.connect('dau_tracking_default.db')
    
    # Fetch data
    df = pd.read_sql_query('''
        SELECT 
            strftime('%w', timestamp) as day_of_week,
            strftime('%H', timestamp) as hour_of_day,
            platform,
            COUNT(*) as activity_count
        FROM user_activities
        GROUP BY day_of_week, hour_of_day, platform
    ''', conn)
    
    # One-hot encode categorical variables
    df_encoded = pd.get_dummies(df, columns=['platform'])
    
    # Prepare features and target
    X = df_encoded.drop('activity_count', axis=1)
    y = df_encoded['activity_count']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f'Model Training Score: {train_score:.2f}')
    print(f'Model Testing Score: {test_score:.2f}')
    
    # Predict future activities
    future_scenarios = np.array([
        [0, 9, 1, 0, 0],   # Weekday morning, web
        [5, 14, 0, 1, 0],  # Weekend afternoon, mobile
        [2, 20, 0, 0, 1]   # Midweek evening, desktop
    ])
    
    predictions = model.predict(future_scenarios)
    print('\nPredicted Activity Counts:')
    for scenario, pred in zip(future_scenarios, predictions):
        print(f'Scenario {scenario}: {int(pred)} activities')

advanced_ml_prediction()
        "
    else
        log "${YELLOW}⚠️ Optional ML Dependencies Not Found. Skipping Advanced Predictions.${NC}"
        log "   To enable ML features, install optional dependencies:"
        log "   1. Uncomment ML libraries in requirements.txt"
        log "   2. Run: pip install -r requirements.txt"
    fi
}

# Main workflow
main() {
    log "🚀 Starting DAU Tracking System Data Science Workflow"
    
    validate_environment
    prepare_data
    analyze_data
    ml_predictions
    
    log "✅ Data Science Workflow Complete!"
}

# Execute main function
main
