import requests
url= f"https://ghloc.ifels.dev/go-chi/chi"
response = requests.get(url)
res = response.json()
print(res['loc'])