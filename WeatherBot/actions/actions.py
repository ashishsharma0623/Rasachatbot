from typing import Any, Text, Dict, List
import requests

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database_connectivity import __init__


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        city_slot = next(tracker.get_latest_entity_values("city"), None)
        city = tracker.get_slot("city") or city_slot


        if city:
            weather_data = self.get_weather(city)
            print(f"City: {city}")
            print(f"Weather Data: {weather_data}")      

            if weather_data:
                response = f"The weather in {city} is {weather_data['main']['temp']}°C with {weather_data['weather'][0]['description']}."
            else:
                response = f"Sorry, I couldn't fetch the weather information for {city}."

        else:
            response = f"Sorry, I couldn't fetch the weather information for {city}."

        dispatcher.utter_message(text=response)
        __init__(tracker.get_slot("city"))
        return []

    @staticmethod
    def get_weather(city: str) -> Dict[Text, Any]:
        api_key = "9524bb51cf5f8675427d00260d806fbb"  
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "units": "metric",
            "appid": api_key
        }

        try:
            print(f"API Request URL: {base_url}?{params}")
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            api_response = response.json()
            print(f"API Response: {api_response}")
            return api_response
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            return None  



