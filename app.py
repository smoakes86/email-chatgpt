from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key from environment variable
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/email-webhook", methods=["POST"])
def email_webhook():
    sender = request.form.get("sender")
    subject = request.form.get("subject")
    body = request.form.get("body-plain")

    if not body:
        return jsonify({"error": "Email body is empty"}), 400

    print(f"Email from: {sender}")
    print(f"Subject: {subject}")
    print(f"Body: {body[:200]}...")

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": body}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    print("GPT-4 Reply:")
    print(reply)

    return jsonify({"reply": reply})

@app.route("/", methods=["GET"])
def home():
    return "Email → ChatGPT webhook is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
