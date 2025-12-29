import json
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from parser import parse

load_dotenv()

app = App(
  token=os.getenv("SLACK_BOT_TOKEN"),
  signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

CHANNEL = os.getenv("COUNTING_CHANNEL")

def prime(n):
  ret = True
  if n <= 1:
    ret = False
  else:
    for i in range(2, int(n ** 0.5) + 1):
      if n % i == 0:
        ret = False
        break
  return ret

@app.event("message")
def new_message(event, say, client):
  if event.get("channel") != CHANNEL:
    return

  text = event.get("text")
  text = text.replace("-", "")
  parsed = parse(text)

  with open("number.txt", "r") as f:
    current = int(f.read() or "0")
  with open("user.txt", "r") as f:
    last_user = f.read()

  user_id = event.get("user")
  write = 0

  reactions = []

  if parsed != -1:
    with open("scores.json", "r") as f:
      scores = json.load(f)
    
    if parsed == current + 1 and user_id != last_user:
      reactions.append("white_check_mark")

      if str(parsed).endswith("69"):
        reactions.append("ok_hand")
      
      if str(parsed).endswith("67"):
        reactions.append("sixseven")
      
      if prime(parsed):
        reactions.append("chess_brilliant")
      
      if parsed % 100 == 0:
        reactions.append("tada")
      
      for reaction in reactions:
        client.reactions_add(
          channel=event.get("channel"),
          name=reaction,
          timestamp=event.get("ts")
        )

      write = parsed
      with open("user.txt", "w") as f:
        f.write(user_id)

      scores[user_id] = scores.get(user_id, 0) + 1
      with open("scores.json", "w") as f:
        json.dump(scores, f)
      
    else:
      client.reactions_add(
        channel=event.get("channel"),
        name="bangbang",
        timestamp=event.get("ts")
      )

      if parsed != current + 1:
        client.chat_postEphemeral(
          channel=event.get("channel"),
          user=user_id,
          text=f"No, the next number {current + 1} (but in words obv)"
        )

      write = current
    with open("number.txt", "w") as f:
      f.write(str(write))
  else:
    client.reactions_add(
      channel=event.get("channel"),
      name="thonking",
      timestamp=event.get("ts")
    )

flask = Flask(__name__)
handler = SlackRequestHandler(app)

@flask.route("/slack/events", methods=["POST"])
def slack_events():
  return handler.handle(request)

@flask.route("/commands/override", methods=["POST"])
def override():
  data = request.form
  text = data.get("text", "")
  split = text.split()

  if data.get("user_id") != "U092839T3A7":
    res = {
      "response_type": "ephermeral",
      "text": "you don't have permissions to do this"
    }
    return jsonify(res)
  
  if len(split) != 1 or not split[0].isdigit():
    res = {
      "response_type": "ephemeral",
      "text": "need one argument - number to set"
    }
    return jsonify(res)

  with open("number.txt", "w") as f:
    f.write(split[0])

  app.client.chat_postMessage(
    channel=data.get("channel_id"),
    text=f"counting number updated to {split[0]}"
  )

  res = {
    "response_type": "ephemeral",
    "text": f"success"
  }
  return jsonify(res)

@flask.route("/commands/leaderboard", methods=["POST"])
def leaderboard():
  with open("scores.json", "r") as f:
    scores = json.load(f)
  
  best = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
  
  text = ""
  for i, (user, score) in enumerate(best):
    text += f"{i + 1}. <@{user}>: {score}\n"

  return jsonify({
    "response_type": "ephemeral",
    "text": text
  })

if __name__ == "__main__":
  flask.run(host="0.0.0.0", port=5000)