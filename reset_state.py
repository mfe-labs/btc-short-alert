"""
State Reset Utility - Manually reset the application state
Use this to close any open positions and reset the state after testing
"""
import json
import os
from state_manager import STATE_FILE, load_state, save_state, close_position


def show_current_state():
    """Display the current state"""
    state = load_state()
    print("\n" + "="*50)
    print("CURRENT STATE")
    print("="*50)
    print(f"Position Open: {state['position_open']}")
    if state['position_open']:
        print(f"Entry Price: ${state['entry_price']:,.2f}")
        print(f"Entry Timestamp: {state['entry_timestamp']}")
    else:
        print("Entry Price: None (No position open)")
    print(f"Price History Entries: {len(state['price_history'])}")
    print("="*50 + "\n")


def reset_state():
    """Reset state to default (close position, keep price history)"""
    state = load_state()
    
    if state['position_open']:
        print(f"Closing position at ${state['entry_price']:,.2f}")
        close_position(state)
        save_state(state)
        print("✅ Position closed. State reset.")
    else:
        print("ℹ️  No position is currently open.")
    
    show_current_state()


def reset_all():
    """Reset everything including price history (use with caution)"""
    default_state = {
        "position_open": False,
        "entry_price": None,
        "entry_timestamp": None,
        "price_history": []
    }
    
    save_state(default_state)
    print("✅ State completely reset (including price history).")
    show_current_state()


if __name__ == "__main__":
    import sys
    
    print("\n🔧 State Reset Utility")
    print("-" * 50)
    
    # Show current state first
    show_current_state()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--full":
        # Full reset (including price history)
        response = input("⚠️  This will reset EVERYTHING including price history. Continue? (yes/no): ")
        if response.lower() == 'yes':
            reset_all()
        else:
            print("Cancelled.")
    else:
        # Just close position (keep price history)
        if load_state()['position_open']:
            response = input("Close the current position? (yes/no): ")
            if response.lower() == 'yes':
                reset_state()
            else:
                print("Cancelled.")
        else:
            print("No position to close.")

