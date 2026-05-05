from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_similarity(movies):
    cv = CountVectorizer(tokenizer=lambda x: x.split('|'))
    matrix = cv.fit_transform(movies['genres'])
    similarity = cosine_similarity(matrix)
    return similarity


def recommend_similar(movies, similarity, movie_title, top_n=10):

    if movie_title not in movies['title'].values:
        print("❌ Movie not found")
        return

    idx = movies[movies['title'] == movie_title].index[0]

    distances = similarity[idx]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:top_n+1]

    print("\n🤖 Similar Movies:\n")

    for i in movie_list:
        print(movies.iloc[i[0]].title)