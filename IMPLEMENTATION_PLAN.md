# Bitcoin Short Alert System - Implementation Plan

## Architecture Overview

### Components
1. **Price Monitor**: Fetches BTC/USD price every minute
2. **Detection Engine**: Analyzes 6-hour rolling window for entry/exit signals
3. **State Manager**: Tracks position status, entry price, and price history
4. **Email Service**: Sends alerts via Gmail SMTP
5. **Main Loop**: Orchestrates all components with error handling

## Technology Stack

### APIs & Services
- **Price API**: CoinGecko API (free, no auth required, 10-50 calls/minute limit)
  - Endpoint: `https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd`
  - Alternative: Binance API (if CoinGecko fails)
- **Email**: Gmail SMTP (smtp.gmail.com:587, TLS)
- **Hosting**: Railway.app (Python runtime)

### Dependencies
- `requests` - HTTP requests for price API
- `smtplib` (built-in) - Email sending
- `email` (built-in) - Email formatting
- `json` (built-in) - State persistence
- `datetime` (built-in) - Time handling
- `time` (built-in) - Sleep/delays
- `logging` (built-in) - Error tracking
- `os` (built-in) - Environment variables

## File Structure

```
btc-short-project/
├── main.py                 # Main application entry point
├── config.py               # Configuration management
├── price_monitor.py        # Price fetching logic
├── detection_engine.py     # Signal detection logic
├── email_service.py        # Email sending functionality
├── state_manager.py        # State persistence
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore rules
├── README.md              # Setup and deployment instructions
└── state.json             # Runtime state (gitignored)
```

## Detailed Component Design

### 1. State Manager (`state_manager.py`)
**Purpose**: Persist and manage application state

**State Structure**:
```json
{
  "position_open": false,
  "entry_price": null,
  "entry_timestamp": null,
  "price_history": [
    {"timestamp": "2024-01-01T12:00:00", "price": 45000.0},
    ...
  ]
}
```

**Functions**:
- `load_state()` - Load from JSON file
- `save_state()` - Save to JSON file
- `add_price_to_history(price, timestamp)` - Add new price, remove old (>6hr)
- `open_position(entry_price)` - Set position as open
- `close_position()` - Set position as closed
- `get_6hr_low()` - Get lowest price in last 6 hours

### 2. Price Monitor (`price_monitor.py`)
**Purpose**: Fetch current BTC/USD price

**Functions**:
- `fetch_btc_price()` - Get price from CoinGecko API
  - Retry logic: 3 attempts with exponential backoff
  - Fallback to Binance if CoinGecko fails
  - Returns: `{"price": float, "timestamp": datetime}` or None

**Error Handling**:
- Network errors: Retry with backoff
- API errors: Log and return None
- Rate limiting: Wait and retry

### 3. Detection Engine (`detection_engine.py`)
**Purpose**: Detect entry and exit signals

**Functions**:
- `check_entry_signal(current_price, price_history)` - Check for 4%+ spike
  - Calculate 6hr low
  - Calculate spike % = (current - 6hr_low) / 6hr_low * 100
  - Return True if spike >= 4%
  
- `check_exit_signal(current_price, entry_price)` - Check TP/SL
  - Calculate change % = (current - entry) / entry * 100
  - Return "TP" if change <= -2.5%
  - Return "SL" if change >= 1.5%
  - Return None if no exit signal

### 4. Email Service (`email_service.py`)
**Purpose**: Send email alerts via Gmail SMTP

**Configuration** (from environment):
- `GMAIL_USER` - Gmail address
- `GMAIL_APP_PASSWORD` - Gmail app password (not regular password)
- `ALERT_EMAIL_1` - First recipient
- `ALERT_EMAIL_2` - Second recipient

**Functions**:
- `send_entry_alert(current_price, 6hr_low, spike_pct, entry_price, tp_price, sl_price)`
  - Subject: "🚨 BTC SHORT SIGNAL - [X]% Spike"
  - Body: Formatted with all details
  
- `send_exit_alert(exit_type, entry_price, current_price, pnl_pct)`
  - Subject: "✅ TAKE PROFIT" or "🛑 STOP LOSS"
  - Body: Entry, current, P/L details

**Error Handling**:
- SMTP errors: Log but don't crash
- Continue monitoring even if email fails

### 5. Main Application (`main.py`)
**Purpose**: Orchestrate all components

**Flow**:
1. Load configuration from environment variables
2. Initialize state manager
3. Main loop (runs every 60 seconds):
   a. Fetch current BTC price
   b. If fetch fails, log and continue
   c. Add price to history (remove old entries)
   d. Save state
   
   e. If position is OPEN:
      - Check exit signals (TP/SL)
      - If exit signal: Send email, close position, save state
   
   f. If position is CLOSED:
      - Check entry signal (4% spike)
      - If entry signal: Send email, open position, save state
   
   g. Sleep for 60 seconds (minus execution time)

**Error Handling**:
- Wrap main loop in try/except
- Log all errors
- Continue running on errors (don't crash)
- Graceful shutdown on KeyboardInterrupt

### 6. Configuration (`config.py`)
**Purpose**: Centralized configuration management

**Functions**:
- `load_config()` - Load from environment variables
- Validate required variables are present
- Return config dict

## Deployment Configuration

### Railway.app Setup
1. **Procfile**: `worker: python main.py`
2. **Environment Variables**:
   - `GMAIL_USER`
   - `GMAIL_APP_PASSWORD`
   - `ALERT_EMAIL_1`
   - `ALERT_EMAIL_2`
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `python main.py`

### Local Development
1. Copy `.env.example` to `.env`
2. Fill in environment variables
3. Run: `python main.py`

## Error Handling Strategy

1. **API Failures**: 
   - Retry 3 times with exponential backoff
   - Fallback to alternative API
   - Log error, continue monitoring

2. **Email Failures**:
   - Log error
   - Continue monitoring (don't block on email)

3. **State File Errors**:
   - Initialize default state if file missing/corrupt
   - Log error, continue

4. **Network Issues**:
   - Retry logic in price fetching
   - Continue loop even if one iteration fails

## Testing Considerations

- Test with mock price data
- Test email sending locally
- Test state persistence
- Test edge cases (price history empty, etc.)

## Security Notes

- Never commit `.env` file
- Use Gmail App Password (not regular password)
- Store credentials in Railway environment variables
- Add `state.json` to `.gitignore`

## Performance Considerations

- Price history cleanup: Remove entries older than 6 hours
- Efficient state file I/O (only write when needed)
- Minimal API calls (1 per minute)
- Lightweight logging

## Success Metrics

- ✅ Runs continuously without crashes
- ✅ Detects 4%+ spikes within 1 minute
- ✅ Sends emails within seconds of trigger
- ✅ Handles API failures gracefully
- ✅ Easy Railway deployment (<5 min setup)

