# Setup Steps Guide

## ✅ Step 1: Environment Variables - COMPLETED
Your `.env` file has been created with:
- Gmail: jamiezaklein@gmail.com
- App Password: Configured
- Alert Recipients: jeremyawhite1@gmail.com, ahwahnee.xyz@gmail.com

## Step 2: Install Dependencies

Run this command in your terminal:

```bash
cd /Users/jamieklein/btc-short-project
pip install -r requirements.txt
```

**What this does**: Installs the `requests` library needed to fetch Bitcoin prices from APIs.

**Expected output**: Should show "Successfully installed requests-2.31.0"

---

## Step 3: Test the Application Locally

Before deploying to Railway, let's test it works on your machine:

```bash
python main.py
```

**What to expect**:
- You'll see logs like "Starting Bitcoin Short Alert System..."
- Every minute, you'll see price updates: "Current BTC price: $XX,XXX.XX"
- The system will build up 6 hours of price history before it can detect spikes
- Press `Ctrl+C` to stop when you're ready

**Testing email** (optional):
- Once you see it's fetching prices correctly, you can let it run until it detects a 4% spike
- Or you can temporarily modify the threshold in `detection_engine.py` to test with a smaller spike

**If you see errors**:
- **"Missing required environment variables"**: The `.env` file might not be loading. Make sure you're running from the project directory.
- **"SMTP authentication failed"**: Double-check your Gmail App Password is correct
- **"Failed to fetch price"**: Check your internet connection

---

## Step 4: Deploy to Railway.app

### Sub-step 4.1: Push to GitHub (if not already done)

1. Initialize git (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: BTC Short Alert System"
   ```

2. Create a new repository on GitHub:
   - Go to github.com
   - Click "New repository"
   - Name it (e.g., "btc-short-alert")
   - Don't initialize with README (we already have one)
   - Click "Create repository"

3. Push your code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/btc-short-alert.git
   git branch -M main
   git push -u origin main
   ```
   (Replace YOUR_USERNAME with your GitHub username)

### Sub-step 4.2: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Sign up/Login (use GitHub to connect)
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository (btc-short-alert)

### Sub-step 4.3: Configure Environment Variables in Railway

1. In your Railway project, click on your service
2. Go to the "Variables" tab
3. Click "New Variable" and add each of these:

   - **Variable**: `GMAIL_USER`
     **Value**: `jamiezaklein@gmail.com`

   - **Variable**: `GMAIL_APP_PASSWORD`
     **Value**: `rupyjrzkvtzedvmw`

   - **Variable**: `ALERT_EMAIL_1`
     **Value**: `jeremyawhite1@gmail.com`

   - **Variable**: `ALERT_EMAIL_2`
     **Value**: `ahwahnee.xyz@gmail.com`

4. Railway will automatically redeploy after you add variables

### Sub-step 4.4: Verify Deployment

1. Go to the "Deployments" tab
2. Wait for the build to complete (should show "Active")
3. Go to the "Metrics" tab to see the app is running
4. Click "View Logs" to see the same output you saw locally
5. You should see: "Starting Bitcoin Short Alert System..." and price updates

**That's it!** Your system is now running 24/7 on Railway.

---

## Step 5: Monitor and Verify

### Check Logs Regularly

In Railway:
- Click "View Logs" to see real-time output
- You should see price updates every minute
- After 6 hours, it will start checking for 4% spikes

### Test Email Delivery

Once a signal triggers (or you modify the threshold for testing):
- Check both recipient inboxes (jeremyawhite1@gmail.com and ahwahnee.xyz@gmail.com)
- Check spam folder if you don't see it
- The email should be formatted HTML with all the details

---

## Troubleshooting

### Email Not Sending
- Verify the App Password is correct (no spaces, all lowercase)
- Make sure 2-Step Verification is enabled on your Gmail account
- Check Railway logs for SMTP errors

### App Not Running
- Check Railway "Metrics" to see if it's running
- Check "Deployments" for build errors
- View logs for error messages

### Price Not Fetching
- Check Railway logs for API errors
- CoinGecko might be rate-limiting (it will retry automatically)
- The system has fallback to Binance API

---

## Next Actions

1. **Right now**: Run `pip install -r requirements.txt` to install dependencies
2. **Then**: Run `python main.py` to test locally
3. **Once working**: Follow Step 4 to deploy to Railway
4. **After deployment**: Monitor logs to verify it's running

Need help with any specific step? Let me know!

