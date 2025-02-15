from flask import Flask, request, render_template
import requests, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HEADERS = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/feature", methods=["GET", "POST"])
def promt():
    response_text = ""
    
    if request.method == "POST":
        user_input = request.form["idea"]

        # Format input for clear, direct responses
        formatted_input = (
            "You are a professional startup advisor who provides clear, practical guidance "
            "for launching, growing, and managing businesses, with a focus on tech, gaming, "
            "and AI sectors. Provide responses directly without repeating the user's question. "
            "Ensure your response is thorough, detailed, and step-by-step when applicable.\n\n"
            "Question: " + user_input + "\n\nAnswer:"
        )

        payload = {"inputs": formatted_input}

        # Call Hugging Face API
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        if response.status_code == 200:
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                full_response = result[0].get("generated_text", "").strip()

                # Extract AI response after "Answer:"
                if "Answer:" in full_response:
                    response_text = full_response.split("Answer:", 1)[-1].strip()
                else:
                    response_text = full_response

        else:
            response_text = f"⚠️ Error: {response.status_code} - {response.text}"

    return render_template("promt.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)