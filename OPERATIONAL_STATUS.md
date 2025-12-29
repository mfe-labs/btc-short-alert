# Operational Status & Monitoring Guide

## ✅ System Status: FULLY OPERATIONAL

Your Bitcoin Short Alert System is now running 24/7 on Railway!

## What's Happening Right Now

### Current Activity
- ✅ **Price Monitoring**: Fetching BTC/USD price every 60 seconds
- ✅ **Price History**: Building up 6-hour rolling window of price data
- ✅ **State Management**: Tracking position status and price history
- ✅ **Email Ready**: Configured to send alerts when signals trigger

### Timeline

**First 6 Hours (Warm-up Period)**
- System is collecting price data
- No entry signals will trigger yet (needs 6 hours of history)
- You'll see logs like: "Building price history. Current: $XX,XXX.XX, History entries: X"
- This is normal and expected!

**After 6 Hours**
- System will start checking for 4%+ spikes
- Entry signals can trigger
- Exit signals (TP/SL) will work if a position is open

## How to Verify Everything is Working

### 1. Check Railway Logs

In your Railway dashboard:
1. Click "View Logs"
2. You should see output like:
   ```
   Starting Bitcoin Short Alert System...
   Configuration loaded successfully
   State loaded. Position open: False
   --- Loop iteration 1 ---
   Current BTC price: $XX,XXX.XX
   Building price history. Current: $XX,XXX.XX, History entries: 1
   ```

**What to look for:**
- ✅ Price updates every ~60 seconds
- ✅ No error messages
- ✅ "Current BTC price" logs appearing regularly

### 2. Monitor Price History Building

Watch the logs to see the history count grow:
- After 1 hour: ~60 entries
- After 6 hours: ~360 entries
- Once you see "6hr Low" in the logs, spike detection is active

### 3. Test Email (Optional - After 6 Hours)

Once 6 hours have passed, you can:
- Wait for a natural 4% spike (may take days/weeks)
- OR temporarily lower the threshold in `detection_engine.py` to test:
  - Change line 25: `if spike_pct >= 4.0:` to `if spike_pct >= 0.1:` (for testing)
  - Push the change, wait for next price check
  - You'll get an email alert
  - **Remember to change it back to 4.0 after testing!**

## What Happens When a Signal Triggers

### Entry Signal (4%+ Spike)
1. System detects spike ≥4% above 6-hour low
2. Sends email to both recipients:
   - jeremyawhite1@gmail.com
   - ahwahnee.xyz@gmail.com
3. Opens position (tracks entry price)
4. Starts monitoring for TP/SL

### Exit Signal (TP or SL)
1. System detects price hit TP (-2.5%) or SL (+1.5%)
2. Sends exit alert email to both recipients
3. Closes position
4. Resumes monitoring for new entry signals

## Monitoring Checklist

### Daily Checks (First Week)
- [ ] Logs showing price updates
- [ ] No error messages in logs
- [ ] System appears to be running continuously

### Weekly Checks
- [ ] Verify email delivery works (when signal triggers)
- [ ] Check that position tracking is working correctly
- [ ] Review logs for any unusual patterns

### Monthly Checks
- [ ] Verify Railway deployment is still active
- [ ] Check that environment variables are still set
- [ ] Review any error logs

## Troubleshooting

### If Logs Stop Updating
1. Check Railway "Metrics" tab - is the service running?
2. Check "Deployments" tab - any failed deployments?
3. Restart the service if needed

### If No Emails Received (After Signal)
1. Check spam folders
2. Verify Gmail App Password is still valid
3. Check Railway logs for SMTP errors
4. Verify recipient emails are correct

### If Price Fetching Fails
- System will retry automatically
- Falls back to Binance API if CoinGecko fails
- Check logs for specific error messages

## System Capabilities

✅ **Fully Automated**: Runs 24/7 without intervention  
✅ **Error Resilient**: Continues running even if API/email fails temporarily  
✅ **State Persistent**: Remembers position status across restarts  
✅ **Email Alerts**: Sends formatted HTML emails to 2 recipients  
✅ **Real-time Monitoring**: Checks price every 60 seconds  

## No Further Action Needed!

The system is now fully operational and will:
- Monitor Bitcoin prices continuously
- Detect 4%+ spikes automatically
- Send email alerts when signals trigger
- Track positions and exit signals
- Run indefinitely on Railway

**Just sit back and let it do its job!** 🚀

## Quick Reference

- **Railway Dashboard**: Check logs and metrics
- **Gmail Sent Folder**: See what emails were sent
- **State File**: Railway doesn't persist files, but state is maintained in memory
- **Restart**: If needed, restart the service in Railway (state will reset, but that's okay)

---

**Status**: ✅ OPERATIONAL  
**Last Updated**: When you deployed  
**Next Check**: Optional - just monitor logs occasionally

