import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json
import os

class DAUReport:
    def __init__(self, db_path: str = 'dau_tracking.db', output_dir: str = 'reports'):
        self.db_path = db_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def get_dau_trend(self, days: int = 30) -> List[Dict[str, int]]:
        """Get Daily Active Users trend over specified days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT 
                    date(timestamp) as activity_date, 
                    COUNT(DISTINCT user_id) as daily_active_users
                FROM user_activities
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY activity_date
                ORDER BY activity_date
            ''', (start_date.isoformat(), end_date.isoformat()))

            return [
                {
                    'date': row[0], 
                    'daily_active_users': row[1]
                } for row in cursor.fetchall()
            ]

    def get_activity_distribution(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, int]:
        """Get distribution of unique users across different activity types"""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=30)
        if end_date is None:
            end_date = datetime.now()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT 
                    activity_type, 
                    COUNT(DISTINCT user_id) as unique_users,
                    COUNT(*) as total_activities
                FROM user_activities
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY activity_type
            ''', (start_date.isoformat(), end_date.isoformat()))

            return {
                row[0]: {
                    'unique_users': row[1],
                    'total_activities': row[2]
                } for row in cursor.fetchall()
            }

    def get_platform_performance(self, days: int = 30) -> Dict[str, Dict[str, Any]]:
        """Analyze performance across different platforms"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT 
                    platform, 
                    COUNT(DISTINCT user_id) as unique_users,
                    COUNT(*) as total_activities,
                    AVG(LENGTH(metadata)) as avg_metadata_size
                FROM user_activities
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY platform
            ''', (start_date.isoformat(), end_date.isoformat()))

            return {
                row[0]: {
                    'unique_users': row[1],
                    'total_activities': row[2],
                    'avg_metadata_size': row[3]
                } for row in cursor.fetchall()
            }

    def generate_comprehensive_report(self, days: int = 30) -> Dict[str, Any]:
        """Generate a comprehensive report of DAU metrics"""
        report = {
            'dau_trend': self.get_dau_trend(days),
            'activity_distribution': self.get_activity_distribution(),
            'platform_performance': self.get_platform_performance(days),
            'report_generated_at': datetime.now().isoformat()
        }

        # Save report to JSON file
        report_path = os.path.join(self.output_dir, f'dau_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        return report

    def export_csv(self, data: List[Dict[str, Any]], filename: str):
        """Export data to CSV for external analysis"""
        import csv
        csv_path = os.path.join(self.output_dir, filename)
        
        if not data:
            return

        with open(csv_path, 'w', newline='') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in data:
                writer.writerow(row)

def main():
    report = DAUReport()
    
    # Generate and print comprehensive report
    comprehensive_report = report.generate_comprehensive_report()
    
    print(" DAU Trend:")
    for day in comprehensive_report['dau_trend']:
        print(f"{day['date']}: {day['daily_active_users']} users")
    
    print("\n Activity Distribution:")
    for activity, stats in comprehensive_report['activity_distribution'].items():
        print(f"{activity}: {stats['unique_users']} unique users, {stats['total_activities']} total activities")
    
    print("\n Platform Performance:")
    for platform, performance in comprehensive_report['platform_performance'].items():
        print(f"{platform}: {performance['unique_users']} unique users, {performance['total_activities']} total activities")

if __name__ == '__main__':
    main()
