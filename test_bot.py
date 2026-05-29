import requests

# Paste your copied tokens inside the quotation marks
BOT_TOKEN = "8830905143:AAHQOdZ3mekUkklCuSxPTj0B45J-nljNDyI"
CHAT_ID = "6582891029"

url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": "🚀 Success! Your VS Code python script is connected to Telegram."
}

try:
    response = requests.post(url, json=payload)
    print("Message sent! Check your Telegram app.")
except Exception as e:
    print(f"Error: {e}")
