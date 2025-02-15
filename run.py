from flask import Flask, request, render_template,jsonify
import requests, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HEADERS = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/promt",methods=["GET"])
def promt():
    return render_template("promt.html")

@app.route("/advisor", methods=["POST"])
def advisor():
    try:
        response_text = ""
        
        if request.method == "POST":
            data = request.json
            user_input = data.get('input')

            if not user_input:
                return jsonify({'error': 'No input provided'}), 400

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

                    return jsonify({"response": response_text})

            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/validate', methods=['POST'])
def validate():
    try:
        data = request.json
        user_input = data.get('input')

        if not user_input:
            return jsonify({'error': 'No input provided'}), 400

        # Properly formatted prompt to reduce input echo
        formatted_input = (
            "You are an expert in startup evaluations. Analyze the following startup idea by "
            "assessing its market potential, strengths, weaknesses, and growth opportunities. "
            "Provide only the analysis in paragraph form without repeating the input idea.\n\n"
            "Startup Idea: " + user_input + "\n\nAnalysis:"
        )

        response = requests.post(API_URL, headers=HEADERS, json={"inputs": formatted_input})

        if response.status_code == 200:
            result = response.json()

            if isinstance(result, list) and len(result) > 0:
                full_response = result[0].get('generated_text', '').strip()

                # Extract AI response after "Analysis:" to prevent input echo
                if "Analysis:" in full_response:
                    ai_response = full_response.split("Analysis:", 1)[-1].strip()
                else:
                    ai_response = full_response

                return jsonify({"response": ai_response})

        return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)