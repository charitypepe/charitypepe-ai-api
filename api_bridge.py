from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Информация от сайта (можеш да я актуализираш ръчно или чрез скрейпинг)
CPEPE_INFO = """
$CPEPE е DeFi екосистема, стартираща на 7 март 2025 г. с общ запас от 1 трилион токена.
За да купите $CPEPE:
1. Посетете https://charitypepe.com
2. Свържете MetaMask или друг Ethereum портфейл
3. Участвайте в пресейла: Pre-sale 1 - $0.0001, Pre-sale 2 - $0.0002
4. Очаквайте до 20x-22x възвръщаемост след листинг!
"""

@app.route("/send_to_bot", methods=["POST"])
def send_to_bot():
    data = request.json
    message = data.get("message")
    source = data.get("source", "unknown")

    try:
        # Обработваме съобщението директно с OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are an AI assistant for CharityPEPE ($CPEPE), an ERC-20 token on Ethereum. Answer in English or Bulgarian based on the message. Use this info:\n\n{CPEPE_INFO}"},
                {"role": "user", "content": message}
            ]
        )
        bot_response = response.choices[0].message.content
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)