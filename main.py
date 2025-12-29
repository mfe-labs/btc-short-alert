"""
Bitcoin Short Alert System - Main Application
Monitors BTC/USD price and sends email alerts for short opportunities
"""
import time
import logging
from datetime import datetime

from config import load_config
from state_manager import (
    load_state, save_state, add_price_to_history,
    open_position, close_position, get_6hr_low
)
from price_monitor import fetch_btc_price
from detection_engine import (
    check_entry_signal, check_exit_signal, calculate_target_prices
)
from email_service import send_entry_alert, send_exit_alert


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def main():
    """Main application loop"""
    logger.info("Starting Bitcoin Short Alert System...")
    
    # Load configuration
    try:
        config = load_config()
        logger.info("Configuration loaded successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return
    
    # Load initial state
    state = load_state()
    logger.info(f"State loaded. Position open: {state['position_open']}")
    
    # Main monitoring loop
    loop_count = 0
    while True:
        try:
            loop_count += 1
            logger.info(f"--- Loop iteration {loop_count} ---")
            
            # Fetch current BTC price
            price_data = fetch_btc_price()
            
            if price_data is None:
                logger.warning("Failed to fetch price. Retrying in next cycle...")
                time.sleep(60)
                continue
            
            current_price = price_data['price']
            timestamp = price_data['timestamp']
            
            logger.info(f"Current BTC price: ${current_price:,.2f}")
            
            # Add price to history and clean up old entries
            add_price_to_history(current_price, timestamp, state)
            save_state(state)
            
            # Check signals based on position status
            if state['position_open']:
                # Position is open - check for exit signals
                entry_price = state['entry_price']
                exit_signal = check_exit_signal(current_price, entry_price)
                
                if exit_signal:
                    # Calculate P/L
                    pnl_pct = ((current_price - entry_price) / entry_price) * 100
                    
                    logger.info(
                        f"{exit_signal} triggered! Entry: ${entry_price:,.2f}, "
                        f"Current: ${current_price:,.2f}, P/L: {pnl_pct:.2f}%"
                    )
                    
                    # Send exit alert
                    send_exit_alert(
                        config['gmail_user'],
                        config['gmail_app_password'],
                        config['recipients'],
                        exit_signal,
                        entry_price,
                        current_price,
                        pnl_pct
                    )
                    
                    # Close position
                    close_position(state)
                    save_state(state)
                    logger.info("Position closed")
                else:
                    logger.info(
                        f"Position open. Entry: ${entry_price:,.2f}, "
                        f"Current: ${current_price:,.2f}, "
                        f"Change: {((current_price - entry_price) / entry_price) * 100:.2f}%"
                    )
            else:
                # Position is closed - check for entry signals
                signal_triggered, six_hr_low, spike_pct = check_entry_signal(
                    current_price,
                    state['price_history']
                )
                
                if signal_triggered:
                    logger.info(
                        f"Entry signal triggered! Spike: {spike_pct:.2f}%, "
                        f"6hr Low: ${six_hr_low:,.2f}, Current: ${current_price:,.2f}"
                    )
                    
                    # Calculate target prices
                    entry_price = current_price
                    tp_price, sl_price = calculate_target_prices(entry_price)
                    
                    # Send entry alert
                    send_entry_alert(
                        config['gmail_user'],
                        config['gmail_app_password'],
                        config['recipients'],
                        current_price,
                        six_hr_low,
                        spike_pct,
                        entry_price,
                        tp_price,
                        sl_price
                    )
                    
                    # Open position
                    open_position(entry_price, state)
                    save_state(state)
                    logger.info(f"Position opened at ${entry_price:,.2f}")
                else:
                    if six_hr_low:
                        logger.info(
                            f"No entry signal. Current: ${current_price:,.2f}, "
                            f"6hr Low: ${six_hr_low:,.2f}, Spike: {spike_pct:.2f}%"
                        )
                    else:
                        logger.info(
                            f"Building price history. Current: ${current_price:,.2f}, "
                            f"History entries: {len(state['price_history'])}"
                        )
            
            # Sleep for 60 seconds (minus execution time)
            # This ensures we check approximately every minute
            time.sleep(60)
            
        except KeyboardInterrupt:
            logger.info("Received interrupt signal. Shutting down gracefully...")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}", exc_info=True)
            # Continue running even on errors
            time.sleep(60)


if __name__ == "__main__":
    main()

