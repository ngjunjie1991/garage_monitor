import os, sys
from flask import Flask, request
from pymessenger import Bot
from pprint import pprint

PAGE_ACCESS_TOKEN = "EAADdZApZBKIQMBACd3sGBnANKn42PCdQiYyzBdi3BEjkZANCfVeoq5ZAZALFJgXCWAZCZBz4m5b9NMMGp8HUtRkbZCK1PohEFJHxrv6OBHV7NqJg3AZBTuJ7LvrJzsbZBmxQ8ZB96W8LcktJC1YHphUXVDMNrwPxYotxsb1ZB7rFrS3ZBlQZDZD"
APP_SECRET_TOKEN = "16bcb9d11ee40f52876e656b022b03cf"

app = Flask(__name__)
bot = Bot(PAGE_ACCESS_TOKEN, app_secret = APP_SECRET_TOKEN)

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
  try:
    if data['object'] == 'page':
      for entry in data['entry']:
        for event in entry['messaging']:
          sender_id = event['sender']['id']
          recipient = event['recipient']['id']

        if event.get('message'):
          response = event['message'].get('text', '') 
          bot.send_text_message(sender_id, response)
  except:
    response = "Sorry, I don't understand what you mean"
    bot.send_text_message(sender_id, response)

  return "ok", 200

if __name__ == "__main__":
  app.run(debug = True, port = 5000)