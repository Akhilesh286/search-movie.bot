from dotenv import load_dotenv
import requests
import os 

load_dotenv()

class MovieInfo:

    def __init__(self,title) -> None:
        API_KEY = os.getenv('API_KEY')
        base_url = "http://www.omdbapi.com/"
        params = {
            "apikey": API_KEY,
            "s": title  # Specify the movie title
        }

        response = requests.get(base_url, params=params)
        data = response.json()
        self.data = data
        
        # self.Title = data["Title"]
        # self.Year = data["Year"]
        # self.Rated = data["Rated"]
        # self.Released = data["Released"]
        # self.Runtime = data["Runtime"]
        # self.Genre = data["Genre"]
        # self.Director = data["Director"]
        # self.Writer = data["Writer"]
        # self.Actors = data["Actors"]
        # self.Plot = data["Plot"]
        # self.Language = data["Language"]
        # self.Country = data["Country"]
        # self.Awards = data["Awards"]
        # self.Poster = data["Poster"]
        # self.imdbRating = data["imdbRating"]
        # self.BoxOffice = data["BoxOffice"]


class MovieByImdb :
    def __init__(self,imdbID) -> None:
        API_KEY = os.getenv('API_KEY')
        base_url = "http://www.omdbapi.com/"
        params = {
            "apikey": API_KEY,
            "i": imdbID  # Specify the movie title
        }

        response = requests.get(base_url, params=params)
        data = response.json()
        self.data = data
        
        self.Title = data["Title"]
        self.Year = data["Year"]
        self.Rated = data["Rated"]
        self.Released = data["Released"]
        self.Runtime = data["Runtime"]
        self.Genre = data["Genre"]
        self.Director = data["Director"]
        self.Writer = data["Writer"]
        self.Actors = data["Actors"]
        self.Plot = data["Plot"]
        self.Language = data["Language"]
        self.Country = data["Country"]
        self.Awards = data["Awards"]
        self.Poster = data["Poster"]
        self.imdbRating = data["imdbRating"]
        self.BoxOffice = data["BoxOffice"]
        # self.imdbID = data["imdbID"]
