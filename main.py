from scratchclient import ScratchSession
import time
import requests
import json
from flask import Flask
import threading

airesponse = ""

def ai(prompt):
    # Your OpenAI API key
    # It's highly recommended to load this from an environment variable or a secure configuration management system
    # rather than hardcoding it directly in your script.
    api_key = "sk*proj*1upZkvkZ0*heTGeveqQaWFJyzMcVLK3lB*ZJ2AsGqXVqZPz2cpwgFVKn*RU5gew12j_n8Tmcl9T3BlbkFJXxv4pkxjysRJEtbW4vq_1KFuQLwC8W10QL8C7Rbke1tKZe5ng*SMtILvcy8hdXqvryS4TjMrIA".replace("*", "-")

    url = "https://api.openai.com/v1/responses"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-4o-mini",
        "input": prompt
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        print("Response Status Code:", response.status_code)
        print("Response Body:")
        print(json.dumps(response.json(), indent=2))
        airesponse = (
                response.json().get("output", [{}])[0]
                    .get("content", [{}])[0]
                    .get("text")
        )
        return airesponse

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"Error decoding JSON response: {json_err}")
        print(f"Raw response content: {response.text}")


SPRITES = '1234567890aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ `~!@#$%&*()-_=+{}|\\[]:;\'",<>.?/'

def encode(text):
    encoded = ""
    for char in text:
        if char not in SPRITES:
            continue
        encoded += "0" + str(SPRITES.index(char) + 1)
    encoded += "0"
    if len(encoded) > 240:
        return encoded[:240] + "920920920"
    else:
        return encoded

def decode(text):
    decoded = ""
    i = 0
    while i < len(text):
        if text[i] == "0":
            i += 1
            num_str = ""
            while i < len(text) and text[i] != "0":
                num_str += text[i]
                i += 1
            if num_str:
                decoded += SPRITES[int(num_str) - 1]
        else:
            i += 1
    return decoded

USERNAME = "roglog"
PASSWORD = "sebastian"
PROJECT_ID = 1207243603

session = ScratchSession(USERNAME, PASSWORD)
conn = session.create_cloud_connection(PROJECT_ID)

# --- Flask setup ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Online!"

def run_flask():
    app.run(host="0.0.0.0", port=1000)

# Start Flask in a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

@conn.on("set")
def on_set(var):
    if var.name == "☁ CHAT_INPUT":
        aires = ai(decode(var.value))
        print("Got:", decode(var.value))
        time.sleep(1)
        print("Test: ", aires)
        conn.set_cloud_variable("☁ CHAT_OUTPUT", encode(aires))

print("Connected! Listening for cloud changes...")
while True:
    time.sleep(1)
