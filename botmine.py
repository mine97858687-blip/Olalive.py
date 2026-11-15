import time
import threading
import requests
from flask import Flask
from accounts import ACCOUNT

app = Flask(__name__)

# Aapke capture kiye gaye exact aur zaroori mobile headers
HEADERS = {
    "host": "i.olaparty.com",
    "sec-ch-ua-platform": '"Android"',
    "user-agent": "Mozilla/5.0 (Linux; Android 17; CPH2871 Build/CP2A.260605.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/157.0.8103.38 Mobile Safari/537.36 Platform/Android17 APP/yym-olaparty-and5.20.0 Channel/(gp) Model/CPH2871 Browser/Default Language/en Environment/Online NetType/WIFI UserMode/Registered",
    "accept": "application/json, text/plain, */*",
    "sec-ch-ua": '"Not-A.Brand";v="99", "Android WebView";v="157", "Chromium";v="157"',
    "x-deviceid": "c7b77dcbe131494f6e29324c197b1ce8",
    "sec-ch-ua-mobile": "?1",
    "origin": "https://www.olaparty.com",
    "x-requested-with": "com.olaparty.weblogin",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://www.olaparty.com/",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cookie": "ho-did=c7b77dcbe131494f6e29324c197b1ce8"
}

@app.route('/')
def home():
    return f"""
    <html>
        <head><title>OlaParty Keep-Alive Bot</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2 style="color: green;">✅ OlaParty Bot is Running 24/7!</h2>
            <p><b>Target UID:</b> {ACCOUNT.get('uid')}</p>
            <p>Status: Active & Pinging Server</p>
        </body>
    </html>
    """

def keep_alive_worker():
    uid = ACCOUNT.get('uid')
    print(f"[*] Starting background keep-alive worker for UID: {uid}")
    
    # Aapka bataya hua base / host endpoint URL
    target_url = "https://i-875.olaparty.com"
    
    while True:
        try:
            # Server ko active rakhne ke liye request bhej rahe hain
            response = requests.get(target_url, headers=HEADERS, timeout=10)
            print(f"[+] Heartbeat sent for UID: {uid} | Status Code: {response.status_code}")
                
        except Exception as e:
            print(f"[-] Connection warning: {e}")
            
        # Har 40 seconds me request bheji jayegi
        time.sleep(40)

if __name__ == "__main__":
    # Background thread me worker start karein
    bot_thread = threading.Thread(target=keep_alive_worker, daemon=True)
    bot_thread.start()
    
    # Render ke liye Flask server start karein (Port 10000)
    app.run(host='0.0.0.0', port=10000)
            
