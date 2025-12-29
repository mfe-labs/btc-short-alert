"""
Price Monitor - Fetches BTC/USD price from free APIs
"""
import time
import requests
from datetime import datetime
from typing import Optional, Dict


def fetch_btc_price_coingecko() -> Optional[Dict]:
    """Fetch BTC price from CoinGecko API"""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'bitcoin' in data and 'usd' in data['bitcoin']:
            price = data['bitcoin']['usd']
            return {
                "price": float(price),
                "timestamp": datetime.now()
            }
    except Exception as e:
        print(f"CoinGecko API error: {e}")
    
    return None


def fetch_btc_price_binance() -> Optional[Dict]:
    """Fetch BTC price from Binance API (fallback)"""
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'price' in data:
            price = float(data['price'])
            return {
                "price": price,
                "timestamp": datetime.now()
            }
    except Exception as e:
        print(f"Binance API error: {e}")
    
    return None


def fetch_btc_price(max_retries: int = 3) -> Optional[Dict]:
    """
    Fetch BTC/USD price with retry logic and fallback APIs
    
    Args:
        max_retries: Maximum number of retry attempts
        
    Returns:
        Dict with 'price' and 'timestamp' or None if all attempts fail
    """
    # Try CoinGecko first
    for attempt in range(max_retries):
        result = fetch_btc_price_coingecko()
        if result:
            return result
        
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
            time.sleep(wait_time)
    
    # Fallback to Binance
    print("CoinGecko failed, trying Binance...")
    for attempt in range(max_retries):
        result = fetch_btc_price_binance()
        if result:
            return result
        
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt
            time.sleep(wait_time)
    
    print("All price API attempts failed")
    return None

