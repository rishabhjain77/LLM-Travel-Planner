# flight_api_integration.py
import requests
import time


def resolve_airport_entity_id(city_name, retries=3, delay=2):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"
    querystring = {"query": city_name}
    headers = {
        "X-RapidAPI-Key": "e70f6955b4msh2616ea010e97336p18ce07jsna9b1b2e9d2c8",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }

    for attempt in range(retries):
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            if data.get('status'):  # If status is True, assuming success
                # Assuming the response structure includes an array of airports
                if 'data' in data and data['data']:
                    airport_id = data['data'][0]['id']  # Extracting the first airport's ID
                    print(f"Success: Found airport ID {airport_id}")
                    return airport_id
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
    print("Failed to fetch airport ID after multiple attempts.")
    return None

def get_flight_one_way(from_id,to_id,start_date,members,retries=3, delay=2):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-one-way"


    querystring = {"fromId": from_id,
                   "toId": to_id,
                   "departDate": start_date,
                   "adults": members,
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

def get_flight_two_way(from_id,to_id,start_date,return_date,members,retries=3, delay=2):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-roundtrip"

    querystring = {"fromId": from_id,
                   "toId": to_id,
                   "departDate": start_date,
                   "returnDate": return_date,
                   "adults": members,
                   "currency": "USD",
                   "market": "US",
                   "locale": "en-US"}

    headers = {
        "X-RapidAPI-Key": "e70f6955b4msh2616ea010e97336p18ce07jsna9b1b2e9d2c8",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }

    for attempt in range(retries):
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            if data.get('status'):  # If status is True, it's considered a success
                return data  # Returning the successful data
            else:
                print(f"Attempt {attempt + 1}: API responded but with failure status, retrying in {delay} seconds...")
                time.sleep(delay)
        else:
            print(f"HTTP error {response.status_code} encountered, retrying in {delay} seconds...")
            time.sleep(delay)

    print("Failed to fetch two-way flight information after multiple attempts.")
    return None


def flight_detail(itineraryId,token):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/detail"

    querystring = {"itineraryId": itineraryId,
                   "token": token,
                   "currency": "USD",
                   "market": "US",
                   "locale": "en-US"}

    headers = {
        "X-RapidAPI-Key": "e70f6955b4msh2616ea010e97336p18ce07jsna9b1b2e9d2c8",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response

