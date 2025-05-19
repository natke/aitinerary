from flask import Flask, render_template, request, jsonify
import requests
import os
from foundry_local import FoundryLocalManager

app = Flask(__name__)
foundry_manager = FoundryLocalManager()
SERVICE_URI = foundry_manager.service_uri

CITIES = [
    'Paris', 'Rome', 'London', 'New York', 'Tokyo', 'Sydney', 'Dubai',
    'Paris', 'Barcelona', 'Bali', 'Bangkok', 'Marrakech'
]

@app.route('/')
def index():
    return render_template('index.html', cities=CITIES)

@app.route('/get-itinerary', methods=['POST'])
def get_itinerary():
    if foundry_manager.is_service_running():  
        city = request.json['city']
        prompt = f"Create a one-day travel itinerary for {city}. Include 8-10 activities with times. Output a JSON list of activities, each with a name and a description"
        
        response = requests.post(
            f"{SERVICE_URI}/v1/chat/completions",
            headers={
                'Content-Type': 'application/json'
            },
            json={
                'model': 'qwen2.5-1.5b-instruct-generic-gpu',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 2048
            }
        )

        print(f"Response: {response.json()}")

        if response.status_code == 200:
            data = response.json()
            itinerary = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            # Strip out the JSON code block
            itinerary = itinerary.replace('```json', '').replace('```', '')
            print(f"Itinerary: {itinerary}")
            itinerary = jsonify({'itinerary': itinerary})
            return itinerary
        else:
            return jsonify({'error': 'Failed to get itinerary'})
    else:
        return jsonify({'error': 'Foundry service is not started. Please start the service.'})

if __name__ == '__main__':
    app.run(debug=True)
