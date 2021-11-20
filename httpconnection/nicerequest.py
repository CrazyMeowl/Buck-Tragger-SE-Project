import requests

#Auth
#auth / get
'''
r = requests.post('https://bugtracker-api.azurewebsites.net/api/Auth', json={
"userName": "admin",
"password": "admin"
})
print(f"Status Code: {r.status_code}, Response: {r.json()}")
'''

#Customer 
#GetAll / get

'''
r = requests.get('https://bugtracker-api.azurewebsites.net/api/Customer/GetAll')
print(f"Status Code: {r.status_code}, Response: {r.json()}")
'''
#GetID / get
'''
CustomerId = "09b225cf-8f32-489b-8096-8cd6ab042ec9"
r = requests.get('https://bugtracker-api.azurewebsites.net/api/Customer/Get/'+CustomerId)
print(f"Status Code: {r.status_code}, Response: {r.json()}")
'''
#Create / post
'''
r = requests.post('https://bugtracker-api.azurewebsites.net/api/Customer/Create', json={
"id": "string",
"userName": "string",
"password": "string",
"fullName": "string",
"email": "user@example.com",
"birthdate": "2021-11-07T14:34:33.998Z"
})
print(f"Status Code: {r.status_code}, Response: {r.json()}")
'''
string = "random shit"
spacer = "  "
e = 0
for i in string:
    print(e*spacer+i)
    e += 1
