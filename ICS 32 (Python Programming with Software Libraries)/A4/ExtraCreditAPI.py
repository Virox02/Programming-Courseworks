import urllib, json
from urllib import request,error

'''
This API works similarly as the OpenWeather and LastFM APIs. Same procedure is being followed.
This API gives an activity followed by the type of activity and participants required to perform this activity. This
is for people when they get bored and want ideas on what to do. This API randomly shuffles activities so that
an activity is not repeated.
The main class is named 'Bored'. This API does not require any apikey or any other parameter.  

'''
    
class Bored():
    def __init__(self):
        self.activity_data = self.extract_activity_json() #assigning all the data fetched from the API
        if self.activity_data != None:
            self.activity = f"Activity: {self.activity_data['activity']}, Type: {self.activity_data['type']}, Participants: {self.activity_data['participants']}"


    def transclude(self, message:str) -> str: #Replaces keywords in a message with associated API data.
        if self.activity_data != None: #this is for the case of an error for say if there is no internet connection
            if '@extracredit' in message:
                message = message.replace("@extracredit", f"{str(self.activity)}") #activity, type, participants
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

    def extract_activity_json(self): #extracts json and returns an object on form of a dictionary that can be used to get data
        url = "https://www.boredapi.com/api/activity"
        activity_obj = self._download_url(url)
        return activity_obj

    
#if __name__ == '__main__':
 
   
    #bored_data = Bored()
    #post = input("enter a post")
    #print(bored_data.transclude(post))



    
