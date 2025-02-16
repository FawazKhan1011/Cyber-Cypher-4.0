from flask import Flask, request, render_template, jsonify
import requests, os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HEADERS = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/promt", methods=["GET"])
def promt():
    return render_template("promt.html")


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/learnmore')
def learn_more():
    return render_template('learnmore.html')


@app.route('/pitch-deck', methods=['POST'])
def pitch_deck():
    try:
        data = request.json
        user_input = data.get('input')

        if not user_input:
            return jsonify({'error': 'No input provided'}), 400

        prompt = (
            "You are an expert pitch deck advisor. Generate a detailed startup pitch deck, including sections for "
            "Problem, Solution, Market Opportunity, Business Model, Traction, Team, and Financials. "
            f"Startup Details: {user_input}\n\nPitch Deck:"
        )

        # Send request to Hugging Face API
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                full_response = result[0].get("generated_text", "").strip()
                ai_response = full_response.replace(prompt, "").strip()  # Remove echoed input
                return jsonify({"response": ai_response})

        return jsonify({"error": f"API Error: {response.status_code} - {response.text}"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/advisor", methods=["POST"])
def advisor():
    try:
        data = request.json
        user_input = data.get('input')

        if not user_input:
            return jsonify({'error': 'No input provided'}), 400

        # Construct a dynamic prompt
        if "growth strategies" in user_input.lower():
            prompt = (
                "You are a startup growth advisor. Provide 5-6 innovative, actionable growth strategies "
                "for AI, SaaS, and tech startups."
            )
        else:
            prompt = (
                "You are a professional startup advisor specializing in tech, AI, and gaming sectors.\n\n"
                f"User Query: {user_input}\n\nAnswer:"
            )

        # Send request to Hugging Face API
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})

        # Handle the API response
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                full_response = result[0].get("generated_text", "").strip()
                ai_response = full_response.replace(prompt, "").strip()  # Remove echoed input
                return jsonify({"response": ai_response})

        return jsonify({"error": f"API Error: {response.status_code} - {response.text}"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/validate", methods=["POST"])
def validate():
    try:
        data = request.json
        user_input = data.get('input')

        if not user_input:
            return jsonify({'error': 'No input provided'}), 400

        # Construct a validation prompt
        formatted_input = (
            "You are an expert in startup evaluations. Analyze the following startup idea by "
            "assessing its market potential, strengths, weaknesses, and growth opportunities. "
            "Provide the analysis in paragraph form without repeating the input.\n\n"
            f"Startup Idea: {user_input}\n\nAnalysis:"
        )

        # Send request to Hugging Face API
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": formatted_input})

        # Handle the API response
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                full_response = result[0].get("generated_text", "").strip()
                ai_response = full_response.replace(formatted_input, "").strip()  # Remove echoed input
                return jsonify({"response": ai_response})

        return jsonify({"error": f"API Error: {response.status_code} - {response.text}"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
