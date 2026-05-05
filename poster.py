import requests

API_KEY = "dac71233146a9ddac1e43af93c4229ec"

def fetch_movie_details(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
    
    response = requests.get(url)
    data = response.json()
    
    if data['results']:
        movie = data['results'][0]

        poster_path = movie.get('poster_path')
        overview = movie.get('overview')

        poster_url = None
        if poster_path:
            poster_url = "https://image.tmdb.org/t/p/w500/" + poster_path

        return poster_url, overview

    return None, None