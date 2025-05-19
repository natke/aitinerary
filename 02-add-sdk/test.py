import requests

prompt = f"Create a one-day travel itinerary for Adelaide. Include 8-10 activities with times. Return only the itinerary in JSON format."
    
headers={
    'Content-Type': 'application/json'
}

print(headers)

json={
    'model': 'Phi-3.5-mini-instruct-generic-gpu',
    'messages': [{'role': 'user', 'content': prompt}]
}

print(json)

response = requests.post("http://localhost:5272/v1/chat/completions", headers=headers, json=json)

print(f"Response: {response}")
