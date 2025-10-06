"""
Entry point for Render deployment.
"""
import os
import uvicorn
from src.api import app

if __name__ == "__main__":
    # Get port from environment variable with a default (not used on Render)
    port = int(os.environ.get("PORT", 5000))
    # Start the server with the correct host and port
    uvicorn.run(app, host="0.0.0.0", port=port)