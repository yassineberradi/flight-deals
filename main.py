# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes
# to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from pprint import pprint
import datetime

data_manager = DataManager()
flight_search = FlightSearch()
# city = 'Cape Town'
# city = city.title()
# pprint(f"get data : {data_manager.get_data()}")
all_cities = data_manager.get_all_cities()
# pprint(f"get {city} lower price : {data_manager.get_lower_price(city)}")
# data_manager.update_sheety("TESTING")
sheet_data = data_manager.get_data()
# for item in all_cities:
#     city_code = flight_search.get_flight_city_code(item)
#     data_manager.update_sheety(text=city_code, city=item)
ORIGIN_CITY_IATA = "LON"

# calculate date period
period_month = 6
time_now = datetime.datetime.now() + datetime.timedelta(days=1)
time_after_period = datetime.datetime.now() + datetime.timedelta(days=(6 * 30))

# date format dd/mm/yyyy
# time_now = time_now.strftime("%d/%m/%Y")
# time_after_period = time_after_period.strftime("%d/%m/%Y")
print(f"time now: {time_now}")
print(f"time after 6 month: {time_after_period}")

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=time_now,
        to_time=time_after_period
    )