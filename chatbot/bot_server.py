import sys
import os
import config
from flask import Flask, request
from pymessenger2 import Bot
from pprint import pprint

PAGE_ACCESS_TOKEN = config.PAGE_ACCESS_TOKEN
APP_SECRET_TOKEN = config.APP_SECRET_TOKEN
app = Flask(__name__)
bot = Bot(PAGE_ACCESS_TOKEN, app_secret=APP_SECRET_TOKEN)


@app.route('/auth', methods=['GET'])
def webhook_auth():
  if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
    if not request.args.get("hub.verify_token") == "hello_token_success":
      return "Verification token mismatch", 403
    return request.args["hub.challenge"], 200
  return "Hello world", 200


@app.route('/auth', methods=['POST'])
def process_messages():
  data = request.get_json()
  pprint(data)
  if data['object'] == 'page':
    for entry in data['entry']:
      for event in entry['messaging']:
        sender_id = event['sender']['id']
        recipient = event['recipient']['id']

      if event.get('message') and event['message'].get('text', '').lower() == "status":
        print("Sending image")
        img_path = "/home/pi/garage_monitor/saved_images/last_image.png"
        bot.send_image(sender_id, img_path)

  return "ok", 200


if __name__ == "__main__":
  app.run(debug=True, port=5000)
