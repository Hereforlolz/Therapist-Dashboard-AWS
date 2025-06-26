import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core_functions import get_dashboard as get_dashboard_handler

def lambda_handler(event, context):
    return get_dashboard_handler(event, context)
