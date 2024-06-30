import requests
#api endpoint URL
url = "http://api.open-notify.org/iss-now.json"

#send GET request
response = requests.get(url)


#check if the request was successful
if response.status_code == 200:
    print("JSON Response:")
    print(response.json())

else:
    print("Request failed")