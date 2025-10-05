# api/index.py
import sys
import os

# Add the 'backend/src' directory to Python's path
# This is the Vercel equivalent of the PYTHONPATH you set locally
backend_src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend', 'src'))
sys.path.insert(0, backend_src_path)

# Now you can import your FastAPI app
# Vercel will look for a variable named 'app'
from api import app

# The 'app' variable is now exposed for Vercel to use.
# Any request to /api/... will be handled by your FastAPI app.
