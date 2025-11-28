import os
import sys

# Add the current directory to path so we can import backend
# When deployed, os.getcwd() is the root of the function/site
sys.path.append(os.getcwd())

from mangum import Mangum
from backend.main import app

handler = Mangum(app)
