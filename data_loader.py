import pandas as pd

def load_data():
    movies = pd.read_csv('data/movies.csv')
    ratings = pd.read_csv('data/ratings.csv')

    # Extract year
    movies['year'] = movies['title'].str.extract(r'\((\d{4})\)')
    movies['year'] = pd.to_numeric(movies['year'], errors='coerce')

    # Clean title
    movies['title'] = movies['title'].str.replace(r"\(\d{4}\)", "", regex=True)
    movies['title'] = movies['title'].str.strip()

    # Ratings
    avg_ratings = ratings.groupby('movieId', as_index=False)['rating'].mean()
    avg_ratings.rename(columns={'rating': 'avg_rating'}, inplace=True)

    rating_count = ratings.groupby('movieId', as_index=False)['rating'].count()
    rating_count.rename(columns={'rating': 'num_ratings'}, inplace=True)

    # Merge
    movies = pd.merge(movies, avg_ratings, on='movieId')
    movies = pd.merge(movies, rating_count, on='movieId')

    return movies