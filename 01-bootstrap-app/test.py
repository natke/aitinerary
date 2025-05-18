import requests

prompt = f"Create a one-day travel itinerary for Adelaide. Include 8-10 activities with times. Return only the itinerary in JSON format."
    
response = requests.post(
    "http://localhost:5272/v1/chat/completions",
    headers={
        "Content-Type": "application/json"
    },
    json={
        "model": "phi-3.5-mini",
        "messages": [{'role': 'user', 'content': prompt}]
    }
)

print(f"Response: {response}")
