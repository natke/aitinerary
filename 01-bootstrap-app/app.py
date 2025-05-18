from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace with your OpenAI API key
#API_KEY = os.getenv('OPENAI_API_KEY')
SERVICE_URI = os.getenv('SERVICE_URI')


CITIES = [
    'Paris', 'Rome', 'London', 'New York', 'Tokyo', 'Sydney', 'Dubai',
    'Paris', 'Barcelona', 'Bali', 'Bangkok', 'Marrakech'
]

@app.route('/')
def index():
    return render_template('index.html', cities=CITIES)

@app.route('/get-itinerary', methods=['POST'])
def get_itinerary():
    city = request.json['city']
    prompt = f"Create a one-day travel itinerary for {city}. Include 8-10 activities with times. Return only the itinerary in JSON format."
    
    response = requests.post(
        f"{SERVICE_URI}/v1/chat/completions",
        headers={
            'Content-Type': 'application/json'
        },
        json={
            'model': 'phi-3.5-mini',
            'messages': [{'role': 'user', 'content': prompt}]
        }
    )

    print(f"Response: {response}")

    if response.status_code == 200:
        data = response.json()
        itinerary = data.get('choices', [{}])[0].get('message', {}).get('content', '')
        return jsonify({'itinerary': itinerary})
    else:
        return jsonify({'error': 'Failed to get itinerary'})

if __name__ == '__main__':
    app.run(debug=True)
