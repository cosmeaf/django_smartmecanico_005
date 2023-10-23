# utils/location/get_location_info.py
from decouple import config
import requests

API_KEY = config('API_KEY')

def get_location_info(ip_address):
    try:
        response = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip_address}')
        data = response.json()
        if response.status_code == 200:
            location_info = {
                "ip": ip_address,
                "isp": data.get("isp"),
                "country": data.get("country_name"),
                "state": data.get("state_prov"),
                "city": data.get("city"),
                "zipcode": data.get("zipcode"),
            }
            return location_info
        else:
            return {"error": "API returned an error code"}
    except Exception as e:
        return str(e)