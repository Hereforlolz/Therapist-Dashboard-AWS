import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core_functions import generate_insight as generate_insight_handler

def lambda_handler(event, context):
    return generate_insight_handler(event, context)
