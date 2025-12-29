"""
Email Service - Sends alerts via Gmail SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List


def send_email(
    gmail_user: str,
    gmail_password: str,
    recipients: List[str],
    subject: str,
    body: str
) -> bool:
    """
    Send email via Gmail SMTP
    
    Args:
        gmail_user: Gmail address
        gmail_password: Gmail app password
        recipients: List of recipient email addresses
        subject: Email subject
        body: Email body (HTML)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = gmail_user
        msg['To'] = ', '.join(recipients)
        
        # Create HTML body
        html_body = MIMEText(body, 'html')
        msg.attach(html_body)
        
        # Send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
        
        print(f"Email sent successfully to {recipients}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_entry_alert(
    gmail_user: str,
    gmail_password: str,
    recipients: List[str],
    current_price: float,
    six_hr_low: float,
    spike_pct: float,
    entry_price: float,
    tp_price: float,
    sl_price: float
) -> bool:
    """Send entry alert email"""
    subject = f"🚨 BTC SHORT SIGNAL - {spike_pct:.2f}% Spike"
    
    body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #d32f2f;">🚨 Bitcoin Short Entry Signal</h2>
        
        <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
          <h3 style="margin-top: 0;">Signal Details</h3>
          <p><strong>Spike Detected:</strong> {spike_pct:.2f}%</p>
          <p><strong>6-Hour Low:</strong> ${six_hr_low:,.2f}</p>
          <p><strong>Current Price:</strong> ${current_price:,.2f}</p>
        </div>
        
        <div style="background-color: #e7f3ff; padding: 15px; border-left: 4px solid #2196F3; margin: 20px 0;">
          <h3 style="margin-top: 0;">Position Details</h3>
          <p><strong>Suggested Entry Price:</strong> ${entry_price:,.2f}</p>
          <p><strong>Take Profit Target:</strong> ${tp_price:,.2f} (-2.5%)</p>
          <p><strong>Stop Loss Target:</strong> ${sl_price:,.2f} (+1.5%)</p>
        </div>
        
        <p style="color: #666; font-size: 12px; margin-top: 30px;">
          This is an automated alert from the BTC Short Alert System.
        </p>
      </body>
    </html>
    """
    
    return send_email(gmail_user, gmail_password, recipients, subject, body)


def send_exit_alert(
    gmail_user: str,
    gmail_password: str,
    recipients: List[str],
    exit_type: str,
    entry_price: float,
    current_price: float,
    pnl_pct: float
) -> bool:
    """Send exit alert email (TP or SL)"""
    if exit_type == "TP":
        subject = "✅ TAKE PROFIT"
        emoji = "✅"
        color = "#4caf50"
        bg_color = "#e8f5e9"
    else:  # SL
        subject = "🛑 STOP LOSS"
        emoji = "🛑"
        color = "#f44336"
        bg_color = "#ffebee"
    
    body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: {color};">{emoji} {exit_type} Triggered</h2>
        
        <div style="background-color: {bg_color}; padding: 15px; border-left: 4px solid {color}; margin: 20px 0;">
          <h3 style="margin-top: 0;">Position Closed</h3>
          <p><strong>Entry Price:</strong> ${entry_price:,.2f}</p>
          <p><strong>Exit Price:</strong> ${current_price:,.2f}</p>
          <p><strong>P/L Percentage:</strong> <span style="color: {color}; font-weight: bold;">{pnl_pct:+.2f}%</span></p>
        </div>
        
        <p style="color: #666; font-size: 12px; margin-top: 30px;">
          This is an automated alert from the BTC Short Alert System.
        </p>
      </body>
    </html>
    """
    
    return send_email(gmail_user, gmail_password, recipients, subject, body)

