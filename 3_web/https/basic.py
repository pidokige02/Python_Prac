import requests

# response = requests.get("https://google.com")
# print(response.status_code)

response = requests.get("https://jsonplaceholder.typicode.com/users/1")
# print(response.content)
# print(response.text)
# print(response.json())
# print(response.headers)
print(response.headers['Content-Type'])


# response = requests.get("https://jsonplaceholder.typicode.com/posts", params={"userId": "1"})
# for post in response.json():
#     print(post["id"])


response = requests.post("https://jsonplaceholder.typicode.com/users", data={'name': 'Test User'})
print(response.headers['Content-Type'])
print(response.status_code)

response = requests.post("https://jsonplaceholder.typicode.com/users", json={'name': 'Test User'})
print(response.headers['Content-Type'])
print(response.status_code)

