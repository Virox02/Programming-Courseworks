import urllib, json
from urllib import request,error
import time

class OpenWeather():
    def __init__(self, apikey, zipcode, ccode):
        self.zipcode = zipcode
        self.ccode = ccode
        self.set_apikey(apikey) #calling the set_apikey function
        #self.apikey = apikey
        self.weather_data = self.extract_weather_json() #assigning all the weather data fetched from the API
        if self.weather_data != None: #this is for the case of an error for say if there is no internet connection
            self.temperature = self.weather_data['main']['temp']
            self.high_temperature = self.weather_data['main']['temp_max']
            self.low_temperature = self.weather_data['main']['temp_min']
            self.longitude = self.weather_data['coord']['lon']
            self.latitude = self.weather_data['coord']['lat']
            self.description = self.weather_data['weather'][0]['description']
            self.humidity = self.weather_data['main']['humidity']
            self.sunset = time.ctime(self.weather_data['sys']['sunset'])
            self.city = self.weather_data['name']

    def set_apikey(self, apikey:str) -> None: #Sets the apikey required to make requests to a web API.
        self.apikey = apikey

    def transclude(self, message:str) -> str: #Replaces keywords in a message with associated API data.
        if self.weather_data != None:
            if '@high' in message:
                message = message.replace("@high", f"{str(self.high_temperature)}K") #highest temp
            elif '@low' in message:
                message = message.replace("@low", f"{str(self.low_temperature)}K") #lowest temp
            elif '@temp' in message:
                message = message.replace("@temp", f"{str(self.temperature)}K") #temp
            elif '@long' in message:
                message = message.replace("@long", str(self.longitude)) #longitude
            elif '@lat' in message:
                message = message.replace("@lat", str(self.latitude)) #latitude
            elif '@weather' in message:
                message = message.replace("@weather", str(self.description)) #weather description
            elif '@hum' in message:
                message = message.replace("@hum", str(self.humidity)) #humidity
            elif '@sunset' in message:
                message = message.replace("@sunset", str(self.sunset)) #sunset time
            elif '@city' in message:
                message = message.replace("@city", str(self.city)) #city
            return message

        
    
    def _download_url(self, url_to_download: str) -> dict: #returns an object in json form that is the data fetched from the api
        response = None
        r_obj = None

        try:
            response = urllib.request.urlopen(url_to_download)
            json_results = response.read()
            r_obj = json.loads(json_results)

        except urllib.error.HTTPError as e:
            print('Failed to download contents of URL')
            print('Status code: {}'.format(e.code))

        except urllib.error.URLError as f:
            print(f.reason, "error fetching the URL. Pls check your internet connectivity")

        finally:
            if response != None:
                response.close()
        
        return r_obj

    def extract_weather_json(self): #extracts json and returns an object on form of a dictionary that can be used to get data
        url = f"https://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.ccode}&appid={self.apikey}"
        weather_obj = self._download_url(url)
        return weather_obj

    
#if __name__ == '__main__':
 #   zipcode = "92697"
  #  ccode = "US"
    #apikey = "0940956a4df510aeb37bac0c7770841a"
   # apikey = input("Enter your apikey")
    #open_weather = OpenWeather(zipcode,ccode,apikey)
    #post = input("Enter your post")
    #print(open_weather.transclude(post))
    #print(f"The temperature for {zipcode} is {open_weather.temperature} degrees")
    #print(f"The high for today in {zipcode} will be {open_weather.high_temperature} degrees")
    #print(f"The low for today in {zipcode} will be {open_weather.low_temperature} degrees")
    #print(f"The coordinates for {zipcode} are {open_weather.longitude} longitude and {open_weather.latitude} latitude")
    #print(f"The current weather for {zipcode} is {open_weather.description}")
    #print(f"The current humidity for {zipcode} is {open_weather.humidity}")
    #print(f"The sun will set in {open_weather.city} at {open_weather.sunset}")

