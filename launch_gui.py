"""
Quick launcher for NamePlate Studio Pro GUI
Run this to start the application
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run
from src.main import main

if __name__ == "__main__":
    sys.exit(main())
