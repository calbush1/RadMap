import requests

def get_location():
    url = 'https://ipinfo.io/json'
    response = requests.get(url)
    data = response.json()
    
    if 'loc' in data:
        latitude, longitude = data['loc'].split(',')
        return float(latitude), float(longitude)
    else:
        return None

location = get_location()
if location:
    latitude, longitude = location
    print(f'Lattitude: {latitude}, Longitude: {longitude}')
else:
    print('Location data not available')
