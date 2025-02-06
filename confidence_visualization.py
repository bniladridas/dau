import matplotlib.pyplot as plt
from src.dau.learning.predictor import SimpleDAUPredictor
import numpy as np

def visualize_confidence():
    """Create a comprehensive visualization of DAU prediction confidence"""
    predictor = SimpleDAUPredictor()
    predictions = predictor.predict_dau(days_to_predict=14)
    
    # Prepare data for plotting
    dates = [pred['date'] for pred in predictions]
    predicted_dau = [pred['predicted_dau'] for pred in predictions]
    confidence_scores = [pred['confidence_score'] for pred in predictions]
    confidence_levels = [pred['confidence_level'] for pred in predictions]
    
    # Color mapping for confidence levels
    color_map = {
        'low': 'red',
        'medium': 'orange',
        'high': 'green'
    }
    colors = [color_map[pred['confidence_level']] for pred in predictions]
    
    # Create figure with two subplots
    plt.figure(figsize=(15, 10))
    
    # DAU Prediction Subplot
    plt.subplot(2, 1, 1)
    plt.bar(dates, predicted_dau, color=colors)
    plt.title('Daily Active Users (DAU) Prediction with Confidence', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Predicted DAU', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Confidence Score Subplot
    plt.subplot(2, 1, 2)
    plt.bar(dates, confidence_scores, color=colors)
    plt.title('Prediction Confidence Scores', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Confidence Score', fontsize=12)
    plt.xticks(rotation=45)
    plt.ylim(0, 1)  # Confidence score is between 0 and 1
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add color legend
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('dau_confidence_visualization.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Print summary for README
    print("Confidence Visualization Summary:")
    print("--------------------------------")
    for date, dau, conf_score, conf_level in zip(dates, predicted_dau, confidence_scores, confidence_levels):
        print(f"{date}: DAU = {dau}, Confidence = {conf_level} (Score: {conf_score:.2f})")

def main():
    visualize_confidence()

if __name__ == '__main__':
    main()
