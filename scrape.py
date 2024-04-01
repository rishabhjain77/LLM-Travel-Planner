import requests
from bs4 import BeautifulSoup
import os

# The base URL
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
url = "https://www.visittheusa.com"
response = requests.get(url, headers=headers)

city_urls=[]


if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the container with the states and cities
    state_containers = soup.find_all('div', class_='navigation__cities-state')

    # Loop through each state container
    for state in state_containers:
        state_name = state.find('h3').text
        cities = state.find_all('a', class_='navigation__cities-link')

        # Loop through each city within the state
        for city in cities:
            city_name = city.text
            city_url = city['href']
            city_urls.append(city_url)
            #print(f"State: {state_name}, City: {city_name}, URL: {city_url}")
else:
    print(f"Failed to retrieve content, status code: {response.status_code}")

# Replace this with the list of city URLs you've obtained

# Directory to save the documents
save_dir = "./data"  # Change this to your actual directory path
#city_urls = ["https://www.visittheusa.com/destination/birmingham"]

for city_url in city_urls:
    response = requests.get(city_url,headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the intro and body sections
        intro_div = soup.find('div', class_='intro__copy')
        intro_text = intro_div.get_text(strip=True) if intro_div else 'Intro text not found'

        body_div = soup.find('div', class_='destination-body__copy')
        body_text = body_div.get_text(strip=True) if body_div else 'Body text not found'

        # Combine intro and body text, if found
        city_content = f"{intro_text}\n\n{body_text}"
        #intro = soup.find('div', class_='intro_copy').get_text(strip=True)
        #body = soup.find('div', class_='destination-body_copy').get_text(strip=True)

        # Combine intro and body text
        #city_content = f"{intro}\n\n{body}"

        # Create a filename from the URL or another unique identifier
        filename = f"{city_url.split('/')[-1]}.txt"
        file_path = os.path.join(save_dir, filename)

        # Write to a file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(city_content)
    else:
        print(f"Failed to retrieve content from {city_url}, status code: {response.status_code}")

