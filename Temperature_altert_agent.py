import requests
from twilio.rest import Client
from uAgent import uAgent

# Configure your weather API and Twilio credentials
weather_api_key = 'YOUR_WEATHER_API_KEY'
twilio_account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
twilio_auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
twilio_phone_number = 'YOUR_TWILIO_PHONE_NUMBER'
user_phone_number = input('USER_PHONE_NUMBER: ' ) # User's phone number to receive alerts
location = input(' Enter CITY/COUNTRY:')  # Location for weather data (e.g., 'New York,US')
min_temperature = float("Enter the minimum temperature:") # Minimum temperature threshold
max_temperature = float("Enter the maximum temperature:") # Maximum temperature threshold

# Initialize Twilio client
twilio_client = Client(twilio_account_sid, twilio_auth_token)

# Create a function to fetch current weather data
def get_current_temperature():
    weather_url = 'YOUR_TWILIO_WEATHER_URL'
    response = requests.get(weather_url)
    weather_data = response.json()
    current_temperature = weather_data['main']['temp']
    return current_temperature

# Create a function to check and send alerts
def check_temperature_and_send_alert():
    current_temp = get_current_temperature()

    if current_temp < min_temperature:
        message = f"Temperature in {location} is {current_temp}°C, below {min_temperature}°C. Bundle up!"
        send_alert(message)
    elif current_temp > max_temperature:
        message = f"Temperature in {location} is {current_temp}°C, above {max_temperature}°C. Stay cool!"
        send_alert(message)

# Create a function to send SMS alert
def send_alert(message):
    twilio_client.messages.create(
        to=user_phone_number,
        from_=twilio_phone_number,
        body=message
    )

# Create a uAgent that runs the check every 30 minutes
agent = uAgent('TemperatureAlertAgent')
agent.schedule_repeating(30 * 60, check_temperature_and_send_alert)

# Start the agent
agent.start()
