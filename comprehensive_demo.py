import importlib
import sys
import os
import subprocess

def run_script(script_name):
    """
    Run a Python script and capture its output
    
    Args:
        script_name (str): Name of the script to run
    
    Returns:
        str: Output of the script
    """
    print(f"\n{'='*50}")
    print(f"🚀 Running {script_name}")
    print(f"{'='*50}")
    
    try:
        # Use subprocess to run the script
        result = subprocess.run(
            [sys.executable, '-m', script_name.replace('.py', '')], 
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True, 
            text=True
        )
        
        # Print stdout and stderr
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ Errors:")
            print(result.stderr)
        
        return result.stdout
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return ""

def main():
    """
    Run all demo scripts in the DAU tracking project
    """
    print("🌟 Comprehensive DAU Tracking System Demo 🌟")
    
    # List of scripts to run in order
    scripts_to_run = [
        'learning_demo.py',
        'reporting_demo.py', 
        'advanced_usage.py',
        'confidence_visualization.py'
    ]
    
    # Store results for potential further processing
    script_results = {}
    
    # Run each script
    for script in scripts_to_run:
        script_results[script] = run_script(script)
    
    # Generate a summary report
    print("\n🏁 Comprehensive Demo Complete!")
    print("Summary of Key Insights:")
    print("-" * 50)
    
    # Basic summary extraction (you can customize this)
    if 'learning_demo.py' in script_results:
        print("🔮 Prediction Confidence:")
        print("   - Scenarios tested: Default, High Variance, Consistent, Sparse")
    
    if 'reporting_demo.py' in script_results:
        print("📊 Reporting Insights:")
        print("   - DAU Trend tracked over 30 days")
        print("   - Multiple activity types analyzed")
    
    if 'confidence_visualization.py' in script_results:
        print("📈 Confidence Visualization:")
        print("   - Generated DAU prediction visualization")
        print(f"   - Visualization saved as 'dau_confidence_visualization.png'")

if __name__ == '__main__':
    main()
