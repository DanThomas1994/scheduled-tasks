import requests
import smtplib
import os

api_key = os.environ.get("API_KEY") # os.environ.get("API_KEY"). This is a way of hiding certain values.
# API key saved as a string.
open_weather_map_endpoint = "https://api.openweathermap.org/data/2.5/forecast"

# Latitude and longitude for Munich:
Latitude = 48.135124
Longitude = 11.581981

weather_parameters = {
    "lat": Latitude,
"lon": Longitude,
    "appid": api_key,
    "cnt": 4 # A count of 4; shows only the first 4 forecasts.
}

response = requests.get(url=open_weather_map_endpoint, params=weather_parameters)
# print(response.status_code) # 200 means it worked!
response.raise_for_status() # Raise an exception if there is a problem.
# print(response.json()) # Get the data from the website in json format.
weather_data = response.json()
# print(weather_data["list"])

# first_forecast = weather_data["list"][0]["weather"]
# print(first_forecast)
# first_forecast_code = first_forecast[0]["id"]
# print(first_forecast_code)

# Use list comprehension to create a list of the forecast codes:
# Using "" accesses the value from the key:value pair; using square brackets with a number accesses the
# item in that position in the list.
will_rain = False
forecast_codes = [weather_data["list"][forecast_number]["weather"][0]["id"]
                  for forecast_number in range(0,4)]

for condition_code in forecast_codes:
    if condition_code < 700:
        will_rain = True # Change the boolean to True if any one of the codes indicates that it will rain.

if will_rain: # This is a shortened version of if will_rain == True:
    my_email = os.environ.get("MY_EMAIL")
    my_other_email = os.environ.get("SECOND_EMAIL")
    password = os.environ.get("MY_PASSWORD")

    with smtplib.SMTP("smtp.gmail.com") as connection:  # Using the 'with' keyword ensures the connection
        # is closed off automatically (after the email is sent).
        connection.starttls()  # Encrypts the email/makes it secure.
        connection.login(user=my_email, password=password)  # Login to my gmail account.
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_other_email,
            msg="Subject:Weather Report\n\nIt's going to rain today. Bring an umbrella!")
        connection.close()
