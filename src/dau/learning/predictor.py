import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any

class SimpleDAUPredictor:
    def __init__(self, db_path: str = 'dau_tracking.db'):
        self.db_path = db_path

    def _get_historical_dau(self, days: int = 30) -> List[Dict[str, Any]]:
        """Retrieve historical Daily Active Users data"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT 
                    date(timestamp) as activity_date, 
                    COUNT(DISTINCT user_id) as daily_active_users,
                    strftime('%w', timestamp) as day_of_week,
                    strftime('%m', timestamp) as month
                FROM user_activities
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY activity_date
                ORDER BY activity_date
            ''', (start_date.isoformat(), end_date.isoformat()))

            return [
                {
                    'date': row[0], 
                    'dau': row[1],
                    'day_of_week': int(row[2]),
                    'month': int(row[3])
                } for row in cursor.fetchall()
            ]

    def predict_dau(self, days_to_predict: int = 7) -> List[Dict[str, Any]]:
        """Simple DAU prediction based on historical patterns with confidence calculation"""
        historical_data = self._get_historical_dau()
        
        # Basic prediction strategies
        predictions = []
        
        # Strategy 1: Average DAU
        avg_dau = sum(day['dau'] for day in historical_data) / len(historical_data)
        
        # Strategy 2: Day of Week Pattern
        day_of_week_avg = {}
        day_of_week_std = {}
        for day in historical_data:
            day_of_week_avg.setdefault(day['day_of_week'], []).append(day['dau'])
        
        # Calculate mean and standard deviation for each day of week
        day_of_week_stats = {}
        for dow, daus in day_of_week_avg.items():
            mean_dau = sum(daus) / len(daus)
            std_dau = (sum((x - mean_dau) ** 2 for x in daus) / len(daus)) ** 0.5
            day_of_week_stats[dow] = {
                'mean': mean_dau,
                'std': std_dau
            }
        
        for i in range(days_to_predict):
            prediction_date = datetime.now() + timedelta(days=i)
            day_of_week = prediction_date.weekday()
            
            # Blend strategies with weighted average
            day_week_stats = day_of_week_stats.get(day_of_week, {'mean': avg_dau, 'std': 0})
            predicted_dau = (
                avg_dau * 0.4 + 
                day_week_stats['mean'] * 0.6
            )
            
            # Confidence Calculation
            # Lower standard deviation means higher confidence
            confidence_score = 1 - min(1, day_week_stats['std'] / (predicted_dau + 1))
            
            # Adjust confidence based on data richness
            data_points_for_day = len(day_of_week_avg.get(day_of_week, []))
            data_richness_factor = min(1, data_points_for_day / len(historical_data))
            
            confidence_level = (
                confidence_score * 0.7 +  # Prediction stability
                data_richness_factor * 0.3  # Data availability
            )
            
            # Map confidence to descriptive levels
            if confidence_level > 0.8:
                confidence_desc = 'high'
            elif confidence_level > 0.5:
                confidence_desc = 'medium'
            else:
                confidence_desc = 'low'
            
            predictions.append({
                'date': prediction_date.date(),
                'predicted_dau': int(predicted_dau),
                'confidence_score': round(confidence_level, 2),
                'confidence_level': confidence_desc,
                'prediction_details': {
                    'avg_dau': round(avg_dau, 2),
                    'day_of_week_mean': round(day_week_stats['mean'], 2),
                    'day_of_week_std': round(day_week_stats['std'], 2)
                }
            })
        
        return predictions

    def analyze_user_segments(self, days: int = 30) -> Dict[str, Any]:
        """Analyze user segments based on activity frequency"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        with sqlite3.connect(self.db_path) as conn:
            # User activity frequency analysis
            cursor = conn.execute('''
                SELECT 
                    user_id, 
                    COUNT(DISTINCT date(timestamp)) as activity_days,
                    COUNT(*) as total_activities
                FROM user_activities
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY user_id
            ''', (start_date.isoformat(), end_date.isoformat()))

            user_data = cursor.fetchall()

        # Segment users
        segments = {
            'inactive': 0,
            'occasional': 0,
            'regular': 0,
            'power_users': 0
        }

        for _, activity_days, total_activities in user_data:
            if activity_days == 0:
                segments['inactive'] += 1
            elif activity_days <= 3:
                segments['occasional'] += 1
            elif activity_days <= 10:
                segments['regular'] += 1
            else:
                segments['power_users'] += 1

        return {
            'total_users': len(user_data),
            'segments': segments,
            'segment_percentages': {
                segment: count / len(user_data) * 100 
                for segment, count in segments.items()
            }
        }

def main():
    predictor = SimpleDAUPredictor()
    
    # Predict DAU for next week
    print(" DAU Predictions:")
    predictions = predictor.predict_dau()
    for pred in predictions:
        print(f"{pred['date']}: {pred['predicted_dau']} users (Confidence: {pred['confidence_level']})")
    
    # Analyze User Segments
    print("\n User Segment Analysis:")
    segments = predictor.analyze_user_segments()
    print("Total Users:", segments['total_users'])
    print("\nUser Segments:")
    for segment, percentage in segments['segment_percentages'].items():
        print(f"{segment.replace('_', ' ').title()}: {percentage:.2f}%")

if __name__ == '__main__':
    main()
