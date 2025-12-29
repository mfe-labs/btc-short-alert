# Quick Testing Steps (6 Hours From Now)

## ✅ What's Already Done

1. **Thresholds Updated** (ready for production):
   - Entry signal: **3.0%** (changed from 4.0%)
   - Stop loss: **2.5%** (changed from 1.5%)
   - Take profit: **2.5%** (unchanged)

2. **Reset Tools Created**:
   - `reset_state.py` - For local testing
   - `check_state.py` - To view current state
   - Environment variable reset method (easiest for Railway)

## 📋 Steps to Follow (In 6 Hours)

### Step 1: Lower Threshold for Email Test

Edit `detection_engine.py` line 29:
```python
# Change from:
if spike_pct >= 3.0:
# To:
if spike_pct >= 0.1:
```

Then push:
```bash
git add detection_engine.py
git commit -m "Test: Lower threshold to 0.1% for email testing"
git push
```

### Step 2: Wait for Test Email

- Should arrive within minutes (0.1% threshold is very sensitive)
- Check both recipient inboxes
- Verify email formatting looks good

### Step 3: Reset State After Test

**Easiest Method (Railway):**

1. Go to Railway → Your service → Variables tab
2. Add variable: `RESET_STATE` = `true`
3. Wait ~60 seconds (one cycle)
4. Check logs - should see "Position closed. State reset."
5. **Remove the RESET_STATE variable** (or set to `false`)

**Alternative: Restart Service**
- Railway dashboard → Settings → Restart
- This resets everything (including price history, but it rebuilds)

### Step 4: Restore Production Threshold

Edit `detection_engine.py` line 29:
```python
# Change back to:
if spike_pct >= 3.0:
```

Then push:
```bash
git add detection_engine.py
git commit -m "Restore production threshold to 3.0%"
git push
```

## ✅ Final Production Settings

After testing, your system will have:
- **Entry Signal**: 3.0% spike ✅
- **Take Profit**: -2.5% ✅
- **Stop Loss**: +2.5% ✅

## 🎯 That's It!

After these steps, your system is fully configured and ready for production monitoring.

