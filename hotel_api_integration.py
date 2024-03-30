# hotel_api_integration.py
import requests
import time

def resolve_hotel_entity_id(destination,retries=3, delay=2):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/hotels/auto-complete"

    querystring = {"query": destination,
                   "market": "US",
                   "locale": "en-US"}

    headers = {
        "X-RapidAPI-Key": "e70f6955b4msh2616ea010e97336p18ce07jsna9b1b2e9d2c8",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }

    #response = requests.get(url, headers=headers, params=querystring)

    for attempt in range(retries):
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            if data.get('status'):  # If status is True, assuming success
                if 'data' in data and data['data']:
                    hotel_id = data['data'][0]['entityId']  # Extracting the first Location's ID
                    print(f"Success: Found hotel ID {hotel_id}")
                    return hotel_id
                else:
                    print("No data found for the given city name.")
                    return None
            else:
                print(f"Attempt {attempt + 1}: Failed to fetch data, status False, retrying in {delay} seconds...")
                time.sleep(delay)
        else:
            print(f"HTTP error {response.status_code}, retrying in {delay} seconds...")
            time.sleep(delay)

    # After all retries have been exhausted
    print("Failed to fetch hotel ID after multiple attempts.")

    return None

def get_hotel_info(entity_id, checkin, checkout,adults,retries=3, delay=2):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/hotels/search"

    querystring = {"entityId": entity_id,
                   "checkin": checkin,
                   "checkout": checkout,
                   "rooms": "1",
                   "adults": adults,
                   "resultsPerPage": "15",
                   "page": "1",
                   "currency": "USD",
                   "market": "US",
                   "locale": "en-US"}

    headers = {
        "X-RapidAPI-Key": "e70f6955b4msh2616ea010e97336p18ce07jsna9b1b2e9d2c8",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }

    #response = requests.get(url, headers=headers, params=querystring)

    for attempt in range(retries):
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            if data.get('status'):
                return data
            else:
                print(f"Attempt {attempt + 1}: Failed to fetch data, retrying in {delay} seconds...")
                time.sleep(delay)
        else:
            print(f"HTTP error {response.status_code}, retrying in {delay} seconds...")
            time.sleep(delay)

    print("Failed to fetch flight information after multiple attempts.")
    return None
