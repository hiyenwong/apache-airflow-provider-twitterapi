import requests

api_key = "new1_b099c7579e9444ec89d1c0fdcf7c2905"
url = "https://api.twitterapi.io/twitter/tweet/advanced_search"

headers = {"x-api-key": api_key}
params = {"query": "from:elonmusk", "queryType": "Latest", "cursor": ""}

response = requests.get(url, headers=headers, params=params)
data = response.json()
print(data)
