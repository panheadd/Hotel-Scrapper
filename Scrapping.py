import os
import sys
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

# CURRENT URL IS FOR BELOW QUERY
# Rome
# checkin= 2024-06-03
# checkout=2024-06-16
# group_adults=2
# no_rooms=1
# group_children=0

hotels_data = []


def scrap_hotel(city, check_in, check_out):
    hotels_data.clear()
    url = 'https://www.booking.com/searchresults.html?ss='+city+'&checkin='+check_in+'&checkout='+check_out
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/51.0.2704.64 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    hotels = soup.findAll('div', {'data-testid': 'property-card'})

    # Loop over the hotel elements and extract the desired data
    for hotel in hotels:
        # Extract the hotel name
        name_element = hotel.find('div', {'data-testid': 'title'})
        if name_element is not None:
            name = name_element.text.strip()
        else:
            name = "NOT GIVEN"

        address_element = hotel.find('span', {'data-testid': 'address'})
        if address_element is not None:
            address = address_element.text.strip()
        else:
            address = "NOT GIVEN"

        distance_element = hotel.find('span', {'data-testid': 'distance'})
        if distance_element is not None:
            distance = distance_element.text.strip()
        else:
            distance = "NOT GIVEN"

        rating_element = hotel.find('a', {'data-testid': 'secondary-review-score-link'})
        if rating_element is not None:
            rating = rating_element.text.strip()
        else:
            rating = "NOT GIVEN"

        price_element = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
        if price_element is not None:
            price = price_element.text.strip()[3:]
        else:
            price = "NOT GIVEN"

        # Append hotels_data with info about hotel
        hotels_data.append({
            'Name': name,
            'Address': address,
            'Distance': distance,
            'Rating': rating,
            'Price': price
        })

    # sortu burda yapıp csv ye eklenecek

    for hotel in hotels_data:
        price_str = str(hotel.get("Price")).replace(',', '')
        price_int = int(price_str)
        hotel["Price"] = price_int

    hotels = pd.DataFrame(sorted(hotels_data, key=lambda k: k['Price']))
    exe_dir = os.path.dirname(sys.argv[0])
    csv_path = os.path.join(exe_dir, 'test_hotels.csv')
    hotels.head()
    hotels.to_csv(csv_path, header=True, index=False)
