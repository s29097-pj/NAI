# Autorzy: Aleksander Bastek (s27454), Michał Małolepszy (s29097)

#  !--- Opis Problemu ---!
# Celem jest uzyskanie tytułów filmów, które najprawdopodobniej są zgodne lub niezgodne z preferencjami wpisanej osoby
#
# Rozwiązanie problemu polega na:
# - Ustaleniu podobieństwa użytkowników za pomocą cosine similarity
# - wybraniu użytkowników najbardziej podobnych i najmniej podobnych
# - w przypadku rekomendowanych filmów trzeba:
#     a) pobrać filmy najbardziej podobnych użytkowników
#     b) przemnożyć ich oceny razy waga, którą jest stopień podobieństwa
#     c) po normalizacji uzyskujemy szacowaną ocenę od 1-10
#     d) z uzyskanego zbioru bierzemy pięć najlepszych
# - w przypadku nierekomendowanych proces różni się tylko tym, że bierzemy pięć filmów z najmniejszą oceną
#
#  !--- Użycie ---!
# - użyć interpretora python np. "python recommendation_system.py"
# - Wpisać imię i nazwisko szukanej osoby

import pandas as pd
from pandas import Series
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import requests

df = pd.read_csv("recommendations.csv")
user_x_movies = df.pivot_table(index='user_id', columns='movie', values='rating').fillna(0)

# movie               1670  365 dni  ...  Źródło (The Fountain)  Żona na niby
# user_id                            ...
# Adrian Kemski        0.0      0.0  ...                    0.0           0.0
# Aleksander Bastek    0.0      0.0  ...                    0.0           0.0
# Cyprian Czerwiński   0.0      0.0  ...                    0.0           0.0
# ...

user_similarity = cosine_similarity(user_x_movies)
user_x_user = pd.DataFrame(user_similarity,
                           index=user_x_movies.index,
                           columns=user_x_movies.index)

# movie               1670  365 dni  ...  Źródło (The Fountain)  Żona na niby
# user_id                            ...
# Adrian Kemski        0.0      0.0  ...                    0.0           0.0
# Aleksander Bastek    0.0      0.0  ...                    0.0           0.0
# Cyprian Czerwiński   0.0      0.0  ...                    0.0           0.0
# ...

def get_movie_info(title):
    base_url = "https://imdb.iamidiotareyoutoo.com/search?q="
    query_url = base_url + title.replace(" ", "+")

    try:
        response = requests.get(query_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return

    data = response.json()

    if not data.get("description"):
        print("No results found.")
        return

    movie = data["description"][0]

    print("\nMovie Information")
    print("Title:", movie.get("#TITLE", "N/A"))
    print("Year:", movie.get("#YEAR", "N/A"))
    print("IMDB rank:", movie.get("#RANK", "N/A"))
    print("Actors:", movie.get("#ACTORS", "N/A"))
    print("Actors:", movie.get("#ACTORS", "N/A"))
    print("AKA:", movie.get("#AKA", "N/A"))


if __name__ == "__main__":
    target_user = input()
    top_n_recommendations = 5
    top_n_dissuasion = 5

    if target_user not in user_x_movies.index:
        raise ValueError(f"User {target_user} not found in dataset.")

    similar_users = user_x_user[target_user].drop(target_user)

    users_ratings = user_x_movies.drop(target_user)
    weights = similar_users.values
    weighted_ratings = np.dot(weights, users_ratings)
    recommendation_scores = pd.Series(weighted_ratings, index=user_x_movies.columns)

    target_rated_movies = user_x_movies.loc[target_user]
    target_unrated_movies = target_rated_movies[target_rated_movies == 0].index
    recommendations = recommendation_scores.loc[target_unrated_movies].sort_values(ascending=False).replace(0.0, np.nan).dropna()

    top_n_movies: Series = recommendations.head(top_n_recommendations)
    bottom_n_movies: Series = recommendations.tail(top_n_dissuasion).sort_values(ascending=True)

    print(f"\nTop movie recommendations for user {target_user}:")
    print(top_n_movies)

    print(f"\nUnrecommended movies for user {target_user}:")
    print(bottom_n_movies)

    print("-" * 30)
    print("Movies Info")
    print("\nRecommended:")

    for movie in top_n_movies.index:
        get_movie_info(movie)

    print("\nUnrecommended:")
    for movie in bottom_n_movies.index:
        get_movie_info(movie)
