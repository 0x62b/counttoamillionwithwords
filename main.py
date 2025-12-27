import os

from dotenv import load_dotenv
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

load_dotenv()

app = App(
  token=os.getenv("SLACK_BOT_TOKEN"),
  signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

CHANNEL = "C0A5RFXHXJN"

@app.event("message")
def new_message(event, say):
  pass

flask = Flask(__name__)
handler = SlackRequestHandler(app)

@flask.route("/slack/events", methods=["POST"])
def slack_events():
  return handler.handle(request)

if __name__ == "__main__":
  flask.run(host="0.0.0.0", port=5000)