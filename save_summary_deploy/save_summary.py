import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core_functions import save_summary as save_summary_handler

def lambda_handler(event, context):
    return save_summary_handler(event, context)
