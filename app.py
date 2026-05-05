from data_loader import load_data
from recommender import recommend_movies
from ai_model import build_similarity, recommend_similar

# 🔥 ADD THIS (VERY IMPORTANT)
movies = load_data()
similarity = build_similarity(movies)


if __name__ == "__main__":

    print("🎬 Movie Recommendation System")
    print("1. Filter-based")
    print("2. AI-based")

    choice = input("Choose option: ")

    if choice == "1":

        genres = input("Enter genres: ").split(',')
        min_rating = float(input("Min rating: "))
        min_votes = int(input("Min votes: "))
        min_year = int(input("Start year: "))
        max_year = int(input("End year: "))
        top_n = int(input("How many: "))

        results = recommend_movies(
            movies, genres, min_rating, min_votes, min_year, max_year, top_n
        )

        print("\n🎯 Recommended Movies:\n")

        if results.empty:
            print("❌ No movies found")
        else:
            for _, row in results.iterrows():
                print(f"{row['title']} ({int(row['year'])}) - ⭐ {round(row['avg_rating'],2)}")

    elif choice == "2":

        movie_name = input("Enter movie name: ")
        recommend_similar(movies, similarity, movie_name)

    else:
        print("❌ Invalid choice")