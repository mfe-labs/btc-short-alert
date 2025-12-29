"""
State Check Utility - View current application state
"""
from state_manager import load_state


def main():
    state = load_state()
    
    print("\n" + "="*60)
    print("BITCOIN SHORT ALERT SYSTEM - CURRENT STATE")
    print("="*60)
    
    print(f"\n📊 Position Status:")
    if state['position_open']:
        print(f"   ✅ Position OPEN")
        print(f"   Entry Price: ${state['entry_price']:,.2f}")
        print(f"   Entry Time: {state['entry_timestamp']}")
    else:
        print(f"   ❌ Position CLOSED (No active position)")
    
    print(f"\n📈 Price History:")
    print(f"   Entries: {len(state['price_history'])}")
    if state['price_history']:
        from datetime import datetime
        oldest = datetime.fromisoformat(state['price_history'][0]['timestamp'])
        newest = datetime.fromisoformat(state['price_history'][-1]['timestamp'])
        print(f"   Oldest: {oldest.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Newest: {newest.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Range: {(newest - oldest).total_seconds() / 3600:.1f} hours")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()

