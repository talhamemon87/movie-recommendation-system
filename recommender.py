def recommend_movies(movies, selected_genres, min_rating, min_votes, min_year, max_year, top_n):

    filtered = movies.copy()

    filtered = filtered[filtered['avg_rating'] >= min_rating]
    filtered = filtered[filtered['num_ratings'] >= min_votes]

    filtered = filtered[
        (filtered['year'] >= min_year) & (filtered['year'] <= max_year)
    ]

    filtered = filtered[
        filtered['genres'].apply(lambda x: any(g in x for g in selected_genres))
    ]

    filtered = filtered.sort_values(by=['avg_rating', 'num_ratings'], ascending=False)

    return filtered.head(top_n)