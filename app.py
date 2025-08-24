from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "8150864340:AAFDlE_iv1LwrkJQJjhb7uOQfQSk5P79ZUQ"
ADMIN_ID = "7725438622"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

user_count = 1  # নতুন ইউজার সংখ্যা ট্র্যাকিং

@app.route("/", methods=["POST"])
def webhook():
    global user_count
    update = request.get_json()

    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]
        user_id = message["from"]["id"]
        first_name = message["from"].get("first_name", "NoName")
        username = message["from"].get("username", "NoUsername")
        text = message.get("text", "")

        # /start হ্যান্ডল
        if text == "/start":
            welcome_msg = "🌙 এটি একটি ইসলামিক AI বট। এখানে শুধু ইসলামের বিষয়ে কথা বলা যাবে।"
            requests.get(API_URL + "sendMessage", params={"chat_id": chat_id, "text": welcome_msg})

            admin_msg = f"নতুন ইউজার জয়েন করেছে!\n\nName: {first_name}\nUsername: @{username}\nUser ID: {user_id}\nUser Number: {user_count}"
            requests.get(API_URL + "sendMessage", params={"chat_id": ADMIN_ID, "text": admin_msg})

            user_count += 1
            return "ok", 200

        # অন্য মেসেজ হ্যান্ডল
        if text:
            try:
                api_response = requests.get(f"https://botatka.a0001.net/api/nerob.php?msg={text}")
                data = api_response.json()
                reply_text = data.get("text", "❌ কিছু ভুল হয়েছে, আবার চেষ্টা করুন।")
                requests.get(API_URL + "sendMessage", params={"chat_id": chat_id, "text": reply_text})
            except:
                requests.get(API_URL + "sendMessage", params={"chat_id": chat_id, "text": "❌ কিছু ভুল হয়েছে, আবার চেষ্টা করুন।"})

    return "ok", 200

if __name__ == "__main__":
    app.run(debug=True)