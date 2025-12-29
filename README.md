# Bitcoin Short Alert System

Automated monitoring system that sends email alerts when Bitcoin spikes sharply, signaling potential short opportunities.

## Features

- **Real-time Monitoring**: Checks BTC/USD price every 1 minute
- **6-Hour Rolling Window**: Tracks price history for accurate spike detection
- **Entry Signal**: Alerts when BTC pumps ≥4% in any 6-hour period
- **Exit Signals**: 
  - Take Profit: Price drops 2.5% below short entry
  - Stop Loss: Price rises 1.5% above short entry
- **Email Alerts**: Sends formatted HTML emails via Gmail SMTP
- **Error Handling**: Graceful retry on API failures, continues monitoring even if email fails
- **State Persistence**: Tracks position status and price history across restarts

## Prerequisites

- Python 3.8 or higher
- Gmail account with App Password enabled
- Railway.app account (for deployment) or local machine for testing

## Setup Instructions

### 1. Clone/Download the Project

```bash
cd btc-short-project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gmail App Password

1. Go to your Google Account settings
2. Enable 2-Step Verification (if not already enabled)
3. Go to "App passwords" section
4. Generate a new app password for "Mail"
5. Copy the 16-character password

### 4. Set Environment Variables

Create a `.env` file in the project root (or set environment variables in Railway):

```bash
# Gmail SMTP Configuration
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password

# Alert Recipients
ALERT_EMAIL_1=recipient1@example.com
ALERT_EMAIL_2=recipient2@example.com
```

**Important**: Never commit the `.env` file to version control!

### 5. Run Locally

```bash
python main.py
```

The system will start monitoring and logging to the console. Press `Ctrl+C` to stop.

## Deployment to Railway.app

### Quick Deploy (< 5 minutes)

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up/login with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo" (if you've pushed to GitHub)
   - OR select "Empty Project" and connect your repo later

3. **Configure Environment Variables**
   - In your Railway project, go to "Variables" tab
   - Add the following variables:
     - `GMAIL_USER` = your Gmail address
     - `GMAIL_APP_PASSWORD` = your Gmail app password
     - `ALERT_EMAIL_1` = first recipient email
     - `ALERT_EMAIL_2` = second recipient email

4. **Deploy**
   - Railway will automatically detect the `Procfile`
   - It will install dependencies from `requirements.txt`
   - The app will start running as a worker process

5. **Verify Deployment**
   - Check the "Deployments" tab for build logs
   - Check the "Metrics" tab to see the app is running
   - Check logs to verify price monitoring is working

### Railway Configuration

The `Procfile` tells Railway to run the app as a worker:

```
worker: python main.py
```

Railway will:
- Automatically detect Python
- Install dependencies from `requirements.txt`
- Run the worker process continuously
- Keep the app running 24/7

## How It Works

### Monitoring Loop

1. Every 60 seconds, the system:
   - Fetches current BTC/USD price from CoinGecko API (with Binance fallback)
   - Adds price to 6-hour rolling history
   - Removes prices older than 6 hours

2. **If Position is CLOSED:**
   - Checks if current price is ≥4% above 6-hour low
   - If yes: Sends entry alert email and opens position

3. **If Position is OPEN:**
   - Checks if price dropped 2.5% (TP) or rose 1.5% (SL)
   - If yes: Sends exit alert email and closes position

### State Management

The system maintains a `state.json` file that tracks:
- Whether a position is currently open
- Entry price and timestamp
- 6-hour price history

This allows the system to resume correctly after restarts.

### Error Handling

- **API Failures**: Retries 3 times with exponential backoff, falls back to alternative API
- **Email Failures**: Logs error but continues monitoring (doesn't crash)
- **State File Errors**: Creates default state if file is missing/corrupt
- **Network Issues**: Continues loop even if one iteration fails

## Email Alert Examples

### Entry Alert
- **Subject**: 🚨 BTC SHORT SIGNAL - 4.25% Spike
- **Content**: Current price, 6hr low, spike percentage, entry price, TP/SL targets

### Exit Alert (Take Profit)
- **Subject**: ✅ TAKE PROFIT
- **Content**: Entry price, exit price, profit percentage

### Exit Alert (Stop Loss)
- **Subject**: 🛑 STOP LOSS
- **Content**: Entry price, exit price, loss percentage

## File Structure

```
btc-short-project/
├── main.py                 # Main application entry point
├── config.py               # Configuration management
├── price_monitor.py        # Price fetching logic
├── detection_engine.py    # Signal detection logic
├── email_service.py       # Email sending functionality
├── state_manager.py       # State persistence
├── requirements.txt       # Python dependencies
├── Procfile              # Railway deployment config
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── state.json            # Runtime state (auto-generated, gitignored)
```

## Troubleshooting

### Email Not Sending

1. **Verify Gmail App Password**: Make sure you're using an App Password, not your regular Gmail password
2. **Check 2-Step Verification**: App passwords require 2-Step Verification to be enabled
3. **Check Logs**: Look for SMTP error messages in the console/logs

### Price Not Fetching

1. **Check Internet Connection**: The app needs internet access to fetch prices
2. **Check API Status**: CoinGecko and Binance APIs may be temporarily down
3. **Check Logs**: Look for API error messages

### Position Not Tracking

1. **Check state.json**: Verify the file exists and has valid JSON
2. **Check Logs**: Look for state loading/saving errors
3. **Reset State**: Delete `state.json` to start fresh (will lose current position)

## Cost

- **$0/month**: Uses free tier APIs (CoinGecko, Binance)
- **Railway Free Tier**: Includes 500 hours/month free (enough for 24/7 operation)
- **Gmail**: Free SMTP service

## Success Criteria

✅ Runs continuously without manual intervention  
✅ Detects 4%+ 6-hour spikes within 1 minute of occurrence  
✅ Delivers email alerts within seconds of trigger  
✅ Deployable to Railway in <5 minutes  

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions:
1. Check the logs for error messages
2. Verify all environment variables are set correctly
3. Ensure Gmail App Password is configured properly

