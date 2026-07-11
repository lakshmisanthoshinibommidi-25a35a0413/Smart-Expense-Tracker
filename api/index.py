import sys
import os

# Allow serverless function environment to resolve imports from project root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
