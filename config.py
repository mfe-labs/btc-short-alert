"""
Configuration Management - Loads and validates environment variables
"""
import os
from typing import Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def load_config() -> Dict:
    """
    Load configuration from environment variables
    
    Returns:
        Dictionary with configuration values
        
    Raises:
        ValueError: If required environment variables are missing
    """
    config = {
        'gmail_user': os.getenv('GMAIL_USER'),
        'gmail_app_password': os.getenv('GMAIL_APP_PASSWORD'),
        'alert_email_1': os.getenv('ALERT_EMAIL_1'),
        'alert_email_2': os.getenv('ALERT_EMAIL_2'),
    }
    
    # Validate required variables
    missing = []
    if not config['gmail_user']:
        missing.append('GMAIL_USER')
    if not config['gmail_app_password']:
        missing.append('GMAIL_APP_PASSWORD')
    if not config['alert_email_1']:
        missing.append('ALERT_EMAIL_1')
    if not config['alert_email_2']:
        missing.append('ALERT_EMAIL_2')
    
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Please set these in your .env file or Railway environment variables."
        )
    
    # Build recipients list
    config['recipients'] = [config['alert_email_1'], config['alert_email_2']]
    
    return config

