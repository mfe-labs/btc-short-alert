# Testing Guide - Email System & Threshold Updates

## Overview

This guide walks you through:
1. Testing the email system with a low threshold (0.1%)
2. Resetting the state after testing
3. Updating thresholds to production values (3.0% spike, 2.5% stop loss)

## Current Production Thresholds (After Update)

- **Entry Signal**: 3.0% spike (changed from 4.0%)
- **Take Profit**: -2.5% (unchanged)
- **Stop Loss**: +2.5% (changed from 1.5%)

## Step-by-Step Testing Process

### Step 1: Prepare for Testing (Before 6 Hours)

The system needs 6 hours of price history before it can detect spikes. Wait until you see in the logs:
- "6hr Low: $XX,XXX.XX" (not "Building price history")
- This means spike detection is active

### Step 2: Lower Threshold for Testing

**On Railway:**
1. Go to your Railway project
2. Click on your service
3. Go to "Variables" tab
4. You'll need to modify the code temporarily

**OR Better: Edit Locally and Push:**

1. Edit `detection_engine.py` line 29:
   ```python
   # Change from:
   if spike_pct >= 3.0:
   # To:
   if spike_pct >= 0.1:
   ```

2. Commit and push:
   ```bash
   git add detection_engine.py
   git commit -m "Temporarily lower threshold for email testing"
   git push
   ```

3. Railway will auto-deploy the change

### Step 3: Wait for Test Email

- The system checks every 60 seconds
- With 0.1% threshold, it should trigger very quickly (likely within minutes)
- You'll receive emails at:
  - jeremyawhite1@gmail.com
  - ahwahnee.xyz@gmail.com

### Step 4: Reset State After Testing

**Important**: After the test email triggers, a position will be opened. You need to reset it.

**Option A: Using the Reset Script (Local)**

If you have access to the Railway file system (you don't), you'd use:
```bash
python reset_state.py
```

**Option B: Manual Reset via Railway (Recommended)**

Since Railway doesn't persist files, the state is in memory. The easiest way:

1. **Restart the Railway service:**
   - Go to Railway dashboard
   - Click on your service
   - Click "Settings" tab
   - Click "Restart" button
   - This will reset the state (position will close, but price history will rebuild)

2. **OR wait for natural exit:**
   - The test position will eventually hit TP or SL
   - But this might take a while with 0.1% threshold

**Option C: Reset via Environment Variable (Easiest for Railway)**

The code now supports resetting state via environment variable:

1. Go to Railway dashboard → Your service → Variables tab
2. Add new variable:
   - **Variable**: `RESET_STATE`
   - **Value**: `true`
3. Railway will automatically redeploy
4. Wait ~60 seconds for one cycle
5. Check logs - you should see "Position closed. State reset."
6. **Remove the RESET_STATE variable** (or set it to `false`)
7. Railway will redeploy again

This is the cleanest method - no code changes needed!

### Step 5: Restore Production Thresholds

1. Edit `detection_engine.py`:
   - Line 29: Already set to `3.0` (production value)
   - Line 57: Already set to `2.5` (production value)
   - Line 74: Already set to `0.025` (2.5% stop loss)

2. The thresholds are already updated! Just verify:
   ```bash
   # Check the values
   grep -n "spike_pct >=" detection_engine.py
   grep -n "change_pct >=" detection_engine.py
   ```

3. If you changed it to 0.1 for testing, change it back to 3.0

### Step 6: Verify Production Settings

Run the check script locally to verify:
```bash
python check_state.py
```

Or check the code:
- Entry threshold: 3.0% ✅
- Stop loss: 2.5% ✅
- Take profit: 2.5% ✅

## Quick Reference Commands

### Check Current State
```bash
python check_state.py
```

### Reset State (Close Position)
```bash
python reset_state.py
```

### Reset Everything (Including Price History)
```bash
python reset_state.py --full
```

## Testing Checklist

- [ ] Wait 6 hours for price history to build
- [ ] Lower threshold to 0.1% for testing
- [ ] Push changes to Railway
- [ ] Wait for test email (should arrive quickly)
- [ ] Verify email received at both addresses
- [ ] Reset state (restart Railway service or wait for TP/SL)
- [ ] Restore threshold to 3.0%
- [ ] Verify production thresholds are correct
- [ ] System ready for production monitoring

## Important Notes

### Railway State Management
- Railway doesn't persist files between restarts
- State is stored in memory
- Restarting the service resets state
- Price history will rebuild automatically (takes 6 hours)

### After Testing
- The test position will be open
- You can either:
  1. Restart Railway service (quickest)
  2. Wait for natural TP/SL exit
  3. Temporarily add reset code to main.py

### Production Thresholds
- **Entry**: 3.0% spike (more sensitive than original 4.0%)
- **Stop Loss**: 2.5% (wider than original 1.5% - gives more room)
- **Take Profit**: 2.5% (unchanged)

## Troubleshooting

### Test Email Not Received
- Check spam folders
- Verify Gmail App Password is still valid
- Check Railway logs for SMTP errors
- Verify threshold was actually changed (check logs)

### Position Won't Close
- Restart Railway service (resets state)
- Or wait for natural TP/SL exit
- Or temporarily add reset code to main.py

### State Reset Not Working
- Railway doesn't persist files - restart the service
- Or use the temporary reset code method

