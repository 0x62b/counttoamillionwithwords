import os

from dotenv import load_dotenv
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from parser import parse

load_dotenv()

app = App(
  token=os.getenv("SLACK_BOT_TOKEN"),
  signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

CHANNEL = "C0A5RFXHXJN"

@app.event("message")
def new_message(event, say, client):
  if event.get("channel") != CHANNEL:
    return

  text = event.get("text")
  parsed = parse(text)

  with open("number.txt", "r") as f:
    current = int(f.read() or "0")

  write = 0

  if parsed != -1:
    if parsed == current + 1:
      client.reactions_add(
        channel=event.get("channel"),
        name="white_check_mark",
        timestamp=event.get("ts")
      )
      write = parsed
    else:
      client.reactions_add(
        channel=event.get("channel"),
        name="bangbang",
        timestamp=event.get("ts")
      )
      write = current
    with open("number.txt", "w") as f:
      f.write(write)

flask = Flask(__name__)
handler = SlackRequestHandler(app)

@flask.route("/slack/events", methods=["POST"])
def slack_events():
  return handler.handle(request)

if __name__ == "__main__":
  flask.run(host="0.0.0.0", port=5000)