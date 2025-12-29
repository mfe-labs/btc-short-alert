"""
Detection Engine - Detects entry and exit signals
"""
from typing import Optional, List, Dict, Tuple


def check_entry_signal(current_price: float, price_history: List[Dict]) -> Tuple[bool, Optional[float], Optional[float]]:
    """
    Check if entry signal is triggered (3%+ spike in 6-hour window)
    
    Args:
        current_price: Current BTC price
        price_history: List of price entries with 'price' field
        
    Returns:
        Tuple of (signal_triggered, 6hr_low, spike_percentage)
    """
    if not price_history:
        return False, None, None
    
    # Get 6-hour low
    prices = [entry['price'] for entry in price_history]
    six_hr_low = min(prices)
    
    # Calculate spike percentage
    spike_pct = ((current_price - six_hr_low) / six_hr_low) * 100
    
    # Entry signal: 3% or more spike (changed from 4.0%)
    if spike_pct >= 3.0:
        return True, six_hr_low, spike_pct
    
    return False, six_hr_low, spike_pct


def check_exit_signal(current_price: float, entry_price: float) -> Optional[str]:
    """
    Check if exit signal is triggered (TP or SL)
    
    Args:
        current_price: Current BTC price
        entry_price: Position entry price
        
    Returns:
        "TP" for take profit, "SL" for stop loss, or None
    """
    if entry_price is None:
        return None
    
    # Calculate price change percentage
    change_pct = ((current_price - entry_price) / entry_price) * 100
    
    # Take Profit: Price drops 2.5% below entry
    if change_pct <= -2.5:
        return "TP"
    
    # Stop Loss: Price rises 2.5% above entry (changed from 1.5%)
    if change_pct >= 2.5:
        return "SL"
    
    return None


def calculate_target_prices(entry_price: float) -> Tuple[float, float]:
    """
    Calculate take profit and stop loss prices
    
    Args:
        entry_price: Position entry price
        
    Returns:
        Tuple of (take_profit_price, stop_loss_price)
    """
    take_profit = entry_price * (1 - 0.025)  # 2.5% below entry
    stop_loss = entry_price * (1 + 0.025)    # 2.5% above entry (changed from 1.5%)
    return take_profit, stop_loss

