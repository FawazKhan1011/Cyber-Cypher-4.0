from flask import Flask, request, render_template, jsonify
import requests, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HEADERS = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/promt", methods=["GET"])
def promt():
    return render_template("promt.html")


@app.route("/advisor", methods=["POST"])
def advisor():
    try:
        data = request.json
        user_input = data.get('input')

        if not user_input:
            return jsonify({'error': 'No input provided'}), 400

        # Generate growth advice or respond to user question
        if "growth strategies" in user_input.lower():
            prompt = (
                "You are an expert startup growth advisor. Provide 5-6 unique, trending, and actionable strategies "
                "for startups in the tech, AI, and SaaS industries. The strategies should be practical and current."
            )
        else:
            prompt = (
                "You are a professional startup advisor who provides clear, practical guidance "
                "for launching, growing, and managing businesses, with a focus on tech, gaming, "
                "and AI sectors. Provide responses directly without repeating the user's question. "
                "Ensure your response is thorough, detailed, and step-by-step when applicable.\n\n"
                f"Question: {user_input}\n\nAnswer:"
            )

        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                full_response = result[0].get("generated_text", "").strip()
                response_text = full_response.split("Answer:", 1)[-1].strip() if "Answer:" in full_response else full_response
                return jsonify({"response": response_text})

        return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/validate", methods=["POST"])
def validate():
    try:
        data = request.json
        user_input = data.get('input')

        if not user_input:
            return jsonify({'error': 'No input provided'}), 400

        formatted_input = (
            "You are an expert in startup evaluations. Analyze the following startup idea by "
            "assessing its market potential, strengths, weaknesses, and growth opportunities. "
            "Provide only the analysis in paragraph form without repeating the input idea.\n\n"
            f"Startup Idea: {user_input}\n\nAnalysis:"
        )

        response = requests.post(API_URL, headers=HEADERS, json={"inputs": formatted_input})

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                full_response = result[0].get('generated_text', '').strip()
                ai_response = full_response.split("Analysis:", 1)[-1].strip() if "Analysis:" in full_response else full_response
                return jsonify({"response": ai_response})

        return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
