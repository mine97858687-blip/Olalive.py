import time
import threading
import requests
from flask import Flask
from accounts import ACCOUNT

app = Flask(__name__)

# Aapke capture kiye hue authentic mobile headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 17; CPH2871 Build/CP2A.260605.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/157.0.8103.38 Mobile Safari/537.36 Platform/Android17 APP/yym-olaparty-and5.20.0 Channel/(gp) Model/CPH2871 Browser/Default Language/en Environment/Online NetType/WIFI UserMode/Registered",
    "origin": "https://www.olaparty.com",
    "referer": "https://www.olaparty.com/",
    "accept": "*/*",
    "x-requested-with": "com.olaparty.weblogin"
}

@app.route('/')
def home():
    return f"""
    <html>
        <head><title>OlaParty Online Bot</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2 style="color: green;">✅ OlaParty Bot is 24/7 Online!</h2>
            <p><b>Target UID:</b> {ACCOUNT.get('uid')}</p>
            <p>Status: Active & Connected via Web Endpoint</p>
        </body>
    </html>
    """

def keep_alive_worker():
    uid = ACCOUNT.get('uid')
    print(f"[*] Starting keep-alive worker for UID: {uid}")
    
    # Aapka captured exact endpoint
    target_url = "https://api.olaparty.com/boss_config/get?key=web-login"
    
    while True:
        try:
            # Server ko active rakhne ke liye request bhej rahe hain
            response = requests.get(target_url, headers=HEADERS, timeout=10)
            
            if response.status_code == 200:
                print(f"[+] Heartbeat sent successfully for UID: {uid} (Status: 200)")
            else:
                print(f"[-] Server returned status code: {response.status_code}")
                
        except Exception as e:
            print(f"[-] Connection warning: {e}")
            
        # Har 40 seconds me request bheji jayegi taaki connection alive rahe
        time.sleep(40)

if __name__ == "__main__":
    # Background thread me worker start karein
    bot_thread = threading.Thread(target=keep_alive_worker, daemon=True)
    bot_thread.start()
    
    # Render ke liye Flask server start karein (Port 10000)
    app.run(host='0.0.0.0', port=10000)
  
