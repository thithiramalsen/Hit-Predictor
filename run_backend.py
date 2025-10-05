# d:/VSCode/GitHub/Hit-Predictor/run_backend.py
import uvicorn
import sys
import os

def main():
    """
    Local development server runner.
    This script sets up the Python path correctly and starts the Uvicorn server,
    mimicking the Vercel deployment environment for consistency.
    """
    # Add the 'backend/src' directory to Python's path
    backend_src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend', 'src'))
    if backend_src_path not in sys.path:
        sys.path.insert(0, backend_src_path)
        print(f"Added to sys.path: {backend_src_path}")

    uvicorn.run("api:app", host="127.0.0.1", port=5000, reload=True)

if __name__ == "__main__":
    main()