from flask import Flask, render_template, request
from requests import post
from foundry_local import FoundryLocalManager

app = Flask(__name__)

manager = FoundryLocalManager()
catalog = manager.list_catalog_models()
cache = manager.list_local_models()

# Load environment variables
BASE_API_URL = manager.service_uri

print(f"Service URI: {BASE_API_URL}")

#@app.route('/')
#def home():
#    return render_template('index.html')

@app.route('/models')
def models():
    return render_template('models.html', models=cache)

@app.route('/', methods=['GET', 'POST'])
def get_itinerary():
    
    if request.method == 'GET':
        return render_template('itinerary.html', city="", activities=[], models=cache)
    else:        
        city = request.form['city']
        model = request.form['model_id']
        print(f"City: {city} Model: {model}")

        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "model": "qwen2.5-1.5b-instruct-generic-cpu",
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
             "max_tokens": 2000
       }
    
    response = post(f"{BASE_API_URL}/v1/chat/completions", headers=headers, json=data)

    print(response)

    # Extract the itinerary
    itinerary = []
    if response.status_code == 200:
        data = response.json()['choices'][0]['message']['content']

        for activity in data.split('•'):
            if activity:
                description = activity.strip()
                if (len(description)):
                    itinerary.append({
                        'description': description
                    })
    else:
        itinerary.append({
            'description': "Error: Unable to fetch itinerary. Please try again."
        })

                
    return render_template('itinerary.html', city=city, activities=itinerary, models=cache)

if __name__ == '__main__':
    app.run(debug=True)                    
    
