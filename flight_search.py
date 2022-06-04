import requests
from flight_data import FlightData

FLIGHT_WIKI_ENDPOINT = "https://tequila-api.kiwi.com"
FLIGHT_WIKI_API_KEY = "Tp0ronSCDEzrgCypcKSkuZcUSJooIYYh"

# tt = "https://tequila-api.kiwi.com/locations/query?term=Paris&locale=en-US"


def get_city_code(city: str):
    headers = {
        "apikey": FLIGHT_WIKI_API_KEY,
    }
    # parameters = {
    #     "term": city,
    #     "locale": "en-US"
    # }
    response = requests.get(f"{FLIGHT_WIKI_ENDPOINT}term={city}&locale=en-US", headers=headers)
    # print(response.text)
    response_json = response.json()
    print(response_json)
    return response_json


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.flight_get_data = {}
        self.city_code = {}

    def get_flight_city_code(self, city: str):
        self.flight_get_data = get_city_code(city)
        verbose = None
        for item in self.flight_get_data["locations"]:
            if item["name"] == city:
                print(f"item: {item['name']}, city: {city}, ")
                self.city_code[city] = item["code"]
                verbose = item["code"]
                return verbose
        return verbose

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"apikey": FLIGHT_WIKI_API_KEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        response = requests.get(
            url=f"{FLIGHT_WIKI_ENDPOINT}/v2/search",
            headers=headers,
            params=query,
        )
        # print(response.text)

        try:
            data = response.json()["data"]
        except IndexError and KeyError:
            print(f"No flights found for {destination_city_code}.")
            return None

        if len(data) < 1:
            print(f"No flights found for {destination_city_code}.")
            return None
        else:
            data = data[0]
        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data