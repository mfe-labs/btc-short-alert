"""
State Manager - Handles persistence of application state
"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional


STATE_FILE = "state.json"


def load_state() -> Dict:
    """Load state from JSON file, create default if missing"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
                # Ensure all required fields exist
                if 'position_open' not in state:
                    state['position_open'] = False
                if 'entry_price' not in state:
                    state['entry_price'] = None
                if 'entry_timestamp' not in state:
                    state['entry_timestamp'] = None
                if 'price_history' not in state:
                    state['price_history'] = []
                return state
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading state: {e}. Creating new state.")
    
    # Return default state
    return {
        "position_open": False,
        "entry_price": None,
        "entry_timestamp": None,
        "price_history": []
    }


def save_state(state: Dict) -> None:
    """Save state to JSON file"""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except IOError as e:
        print(f"Error saving state: {e}")


def add_price_to_history(price: float, timestamp: datetime, state: Dict) -> None:
    """Add price to history and remove entries older than 6 hours"""
    # Add new price entry
    state['price_history'].append({
        "timestamp": timestamp.isoformat(),
        "price": price
    })
    
    # Remove entries older than 6 hours
    cutoff_time = timestamp - timedelta(hours=6)
    state['price_history'] = [
        entry for entry in state['price_history']
        if datetime.fromisoformat(entry['timestamp']) >= cutoff_time
    ]


def get_6hr_low(state: Dict) -> Optional[float]:
    """Get the lowest price in the last 6 hours"""
    if not state['price_history']:
        return None
    
    prices = [entry['price'] for entry in state['price_history']]
    return min(prices)


def open_position(entry_price: float, state: Dict) -> None:
    """Open a position with the given entry price"""
    state['position_open'] = True
    state['entry_price'] = entry_price
    state['entry_timestamp'] = datetime.now().isoformat()


def close_position(state: Dict) -> None:
    """Close the current position"""
    state['position_open'] = False
    state['entry_price'] = None
    state['entry_timestamp'] = None

