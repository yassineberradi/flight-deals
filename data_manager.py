import requests

SHEETY_ENDPOINT = "https://api.sheety.co/8c55e4a599e0a3a3235399ed10afb63f/flightDeals/prices"


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheety_get_data = requests.get(SHEETY_ENDPOINT).json()
        self.all_cities = [item['city'] for item in self.sheety_get_data["prices"]]
        self.data = self.sheety_get_data["prices"]

    def get_data(self) -> list:
        return self.data

    def get_all_cities(self) -> list:
        return self.all_cities

    def get_lower_price(self, city: str):
        for item in self.data:
            if item["city"] == city:
                return item["lowestPrice"]
        return

    def update_sheety(self, text: str, city: str):
        for item in self.data:
            if len(item["iataCode"]) < 1 and item["city"] == city:
                item["iataCode"] = text
                sheet_body = {
                    "price": {
                        "city": item['city'],
                        "iataCode": item['iataCode'],
                        "lowestPrice": item['lowestPrice'],
                        "id": item['id'],
                    }}
                try:
                    requests.put(f"{SHEETY_ENDPOINT}/{item['id']}", json=sheet_body).json()
                except:
                    print("error put request")
                else:
                    print("put request ok")
                    self.__init__()
