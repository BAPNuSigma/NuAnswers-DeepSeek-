import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Gunicorn configuration
bind = "0.0.0.0:8000"
workers = 4
timeout = 120
worker_class = "sync"
accesslog = "-"
errorlog = "-"
loglevel = "info" 
