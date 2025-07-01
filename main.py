import os
import sys
import subprocess

# Add the current directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Run the Streamlit app
if __name__ == "__main__":
    # Set the path to the frontend directory
    frontend_path = os.path.join(current_dir, "frontend", "app.py")
    
    # Run streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", frontend_path, "--server.headless", "true", "--server.port", "8501"])
