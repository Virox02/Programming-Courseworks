import urllib, json
from urllib import request,error

class LastFM():
    def __init__(self, apikey, limit = 10, page=None):
        self.page = page
        self.limit = limit
        self.set_apikey(apikey) #calling the set_apikey function
        #self.apikey = apikey
        self.artists_data = self.extract_artists_json() #assigning all the lastfm data fetched from the API

    def set_apikey(self, apikey:str) -> None: #Sets the apikey required to make requests to a web API.
        self.apikey = apikey

    def transclude(self, message:str) -> str: #Replaces keywords in a message with associated API data.
        if self.artists_data != None: #this is for the case of an error for say if there is no internet connection
            if '@lastfm' in message:
                message = message.replace("@lastfm", str(self.artists_data[0])) #top artist
            elif '@top2' in message:
                message = message.replace("@top2", str(self.artists_data[1])) #2nd top
            elif '@top3' in message:
                message = message.replace("@top3", str(self.artists_data[2])) #3rd top
            elif '@top10' in message:
                message = message.replace("@top10", f"{str(self.artists_data)}") #all top10
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

    def extract_artists_json(self): #extracts json and returns an object in form of a dictionary that can be used to get data
        url = f"http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key={self.apikey}&format=json&limit={self.limit}"
        artists_obj = self._download_url(url)
        if artists_obj != None:
            All = []
            for i in range(0, 9):
                data = f"name: {artists_obj['artists']['artist'][i]['name']} | playcount: {artists_obj['artists']['artist'][i]['playcount']} | listeners: {artists_obj['artists']['artist'][i]['listeners']}"
                All.append(data)
            return All
        else:
            return artists_obj


    
#if __name__ == '__main__':
    
    
    #apikey = "88f192fd5ff2f4231efea975e9e225ae"
    #key = input("Enter your apikey")
    #LastFM.set_apikey(key)
    #last_fm = LastFM(apikey)
    #post = "hello @lastfm"
    #print(last_fm.transclude(post))
    

    



    
