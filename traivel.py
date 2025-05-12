from flask import Flask, render_template, request
from requests import get, post

app = Flask(__name__)

# Load environment variables
BASE_URL = "http://localhost:5272"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/itinerary', methods=['POST'])
def get_itinerary():
    city = request.form['city']
    
    # Make API call to OpenAI
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "model": "deepseek-r1-distill-llama-8b-generic-gpu",
        "messages": [{
            "role": "user",
            "content": f"Create a one day travel itinerary for the city of {city}. Include popular attractions, good places to eat, and fun activities. Make it concise and easy to follow."
        }],
        "temperature": 0.7,
        "metadata": {
            "ep": "webgpu"
        }
    }
    
    response = post(f"{BASE_URL}/v1/chat/completions", headers=headers, json=data)

    print(response.json())

    # Simulate a response for demonstration purposes
    # response = {"choices": [{"message": {"content": "1. Visit the Eiffel Tower - A must-see landmark in Paris.\n2. Lunch at Café de Flore - Enjoy a classic French meal.\n3. Stroll through the Louvre - Explore world-famous art.\n4. Dinner at Le Meurice - Experience fine dining."}}]} 
    # Extract the itinerary
    itinerary = []
    if response.status_code == 200:
        data = response.json()
        for activity in data['choices'][0]['message']['content'].split('\n'):
            if activity:
                parts = activity.split('•')
                if len(parts) >= 2:
                    name = parts[0].strip()
                    description = parts[1].strip()
                    itinerary.append({
                        'name': name,
                        'description': description
                    })
    return render_template('itinerary.html', itinerary=itinerary)

if __name__ == '__main__':
    app.run(debug=True)                    
    
