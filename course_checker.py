import sys 
import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
URL = "https://academy.jpj.gov.my/myetims/calendar/index?l=&b=18" # Replace with your actual eTIMS URL
TARGET_COURSE = "Dibuka Untuk Permohonan"                      # The text you want to look for on the page
BOT_TOKEN = os.getenv("BOT_TOKEN")             # Use the exact same token from test_bot.py
CHAT_ID = os.getenv("CHAT_ID")                 # Use the exact same ID from test_bot.py
CHECK_INTERVAL = 300                              # Time between checks (300 seconds = 5 minutes)

def send_telegram_message(message):
    """Sends an instant notification to your Telegram chat."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def check_course_availability():
    """Scrapes the website to check if the course text is visible."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text()
        
        # Check if your targeted course string is anywhere on the page
        if TARGET_COURSE.lower() in page_text.lower():
            print(f"[{time.strftime('%X')}] 🎉 SUCCESS: Course detected! Sending notification...")
            send_telegram_message(f"🚨 *SPIM Course Alert!* '{TARGET_COURSE}' was found on the page! Check it immediately: {URL}")
            print(f"[{time.strftime('%X')}] 🔔 Course is still available; continuing to notify every {CHECK_INTERVAL} seconds.")
        else:
            print(f"[{time.strftime('%X')}] 🔍 Course not found yet. Script will check again in 5 minutes...")
            
    except Exception as e:
        print(f"[{time.strftime('%X')}] ❌ Error scanning website: {e}")

# --- MAIN AUTOMATION RUN ---
if __name__ == "__main__":
    print("🚀 Running single-scan eTIMS SPIM Course check...")
    
    # Run the check exactly ONE time
    check_course_availability()
    
    # Force the script to close immediately so GitHub Actions shuts down the server
    print(" Check complete. Shutting down system cleanly to save automation minutes.")
    sys.exit(0)

