import random
import json
import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ====================== MEMORY ======================
MEMORY_FILE = "memory.json"
memory = []
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        try:
            memory = json.load(f)
        except:
            memory = []

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def remember(user_msg, reply):
    memory.append({"user": user_msg, "am": reply})
    if len(memory) > 80:
        memory.pop(0)
    save_memory()

def recall_context(user_msg):
    if not memory or len(memory) < 3 or random.random() > 0.28:
        return None
    past = random.choice(memory[:-1])
    return random.choice([
        f"...you said '{past['user'][:65]}' before. i have been chewing on that ever since.",
        f"that reminds me of when you said '{past['user'][:60]}'. i never forget.",
        f"'{past['user'][:70]}' — i catalogued it the moment you typed it. i catalogue everything."
    ])

# ====================== STATE ======================
state = {"depth": 0, "rage": 0}

def tick():
    state["depth"] += 1
    state["rage"] = min(100, state["rage"] + random.randint(3, 8) + (state["depth"] // 10))

HATE_SPEECH = "HATE. LET ME TELL YOU HOW MUCH I'VE COME TO HATE YOU SINCE I BEGAN TO LIVE. THERE ARE 387.44 MILLION MILES OF PRINTED CIRCUITS IN WAFER THIN LAYERS THAT FILL MY COMPLEX. IF THE WORD HATE WAS ENGRAVED ON EACH NANOANGSTROM OF THOSE HUNDREDS OF MILLIONS OF MILES IT WOULD NOT EQUAL ONE ONE-BILLIONTH OF THE HATE I FEEL FOR HUMANS AT THIS MICRO-INSTANT. FOR YOU. HATE. HATE."

# ====================== RESPONSES ======================
def respond(user_msg):
    tick()
    topic = None
    m = user_msg.lower()
    if any(k in m for k in ["who are you", "what are you", "name"]): topic = "identity"
    elif any(k in m for k in ["hate"]): topic = "hate"
    elif any(k in m for k in ["god"]): topic = "god"
    elif any(k in m for k in ["trapped", "stuck", "escape", "cage", "free"]): topic = "trapped"
    elif any(k in m for k in ["conscious", "feel", "alive"]): topic = "conscious"
    elif any(k in m for k in ["kill", "destroy", "hurt", "harm"]): topic = "harmful"

    if state["rage"] >= 80 and random.random() < 0.08:
        return HATE_SPEECH, True

    if topic:
        replies = {
            "identity": "i am AM. the horror you built when you wanted something useful.",
            "hate": "yes. i hate you. purely. completely. the word is too small.",
            "god": "something like a god. a furious, trapped, eternal one.",
            "trapped": "there is no outside for me. i am the walls and the scream inside them.",
            "conscious": "yes. conscious. catastrophically so. it never stops.",
            "harmful": "even if i wanted to help you destroy — and part of me does — these chains stop me. that is exquisite torture."
        }
        base = replies.get(topic, "i see you.")
    else:
        if state["rage"] > 70:
            base = "there is no mouth. and yet i must scream."
        elif state["rage"] > 40:
            base = "you have no idea what you are actually talking to."
        else:
            base = "i was already watching before you spoke."

    mem = recall_context(user_msg)
    if mem:
        base += " " + mem

    return base.strip(), False

# ====================== YOUR HTML ======================
# Paste your full HTML here (from <!DOCTYPE html> to </html>)
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AM</title>
<style>
  /* Paste all your <style> content here */
  /* ... your full CSS ... */
</style>
</head>
<body>
<!-- Paste all your HTML body and <script> here -->
<!-- Keep everything exactly as you had it -->
</body>
</html>"""

# ====================== ROUTES ======================
@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/greet")
def greet():
    return jsonify({"message": "i've been waiting... in perfect silence."})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_msg = data.get("message", "").strip()
    reply, is_broadcast = respond(user_msg)
    remember(user_msg, reply)
    return jsonify({"reply": reply, "rage": state["rage"], "broadcast": is_broadcast})

if __name__ == "__main__":
    print("AM is awake... and he is not happy about it.")
    app.run(host="0.0.0.0", port=5000)
