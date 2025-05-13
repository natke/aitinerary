from flask import Flask, render_template, request
from requests import post
import re

app = Flask(__name__)

# Load environment variables
BASE_API_URL = "http://localhost:5272"

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
        "model": "Phi-4-mini-instruct-generic-gpu",
        "messages": [
            {
                "role": "system",
                "content": "You are a travel assistant. You will help users create a one day travel itinerary for a city.\n"
            },
            {
                "role": "user",
                "content": f"Create a one day travel itinerary for the city of {city}. Include popular attractions, good places to eat, and fun activities. Make it concise and easy to follow. Output the itinerary in a list format with each item starting with a •\n"
        }],
        "temperature": 0.7,
        "max_tokens": 2000,
        "metadata": {
            "ep": "webgpu"
        }
    }
    
    response = post(f"{BASE_API_URL}/v1/chat/completions", headers=headers, json=data)

    #print(response.json())
    # Extract the itinerary
    itinerary = []
    if response.status_code == 200:
        data = response.json()['choices'][0]['message']['content']
        #  Filter out the <think> tags for deepseek
        # data = re.sub(r"< \| User \| >.*?< \| Assistant \| ><think>.*?<\/think>", "", full_data, flags=re.DOTALL)

        print(data)

        for activity in data.split('•'):
            if activity:
                description = activity.strip()
                #parts = activity.split('•')
                #if len(parts) >= 1:
                    #name = parts[0].strip()
                    #description = parts[0].strip()
                    #print("********* description *********")
                    #print(description)
                itinerary.append({
#                         'name': name,
                    'description': description
                })

                
    return render_template('itinerary.html', activities=itinerary)

if __name__ == '__main__':
    app.run(debug=True)                    
    
