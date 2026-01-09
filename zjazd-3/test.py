import requests

def get_movie_info(title):
    base_url = "https://imdb.iamidiotareyoutoo.com/search?q="
    query_url = base_url + title.replace(" ", "+")  # format title for URL

    try:
        response = requests.get(query_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return

    data = response.json()

    if not data.get("description"):  # if no results
        print("No results found.")
        return

    movie = data["description"][0]

    print("\n🎬 Movie Information")
    print("Title:", movie.get("#TITLE", "N/A"))
    print("Year:", movie.get("#YEAR", "N/A"))
    print("IMDB rank:", movie.get("#RANK", "N/A"))
    print("Actors:", movie.get("#ACTORS", "N/A"))
    print("Actors:", movie.get("#ACTORS", "N/A"))
    print("AKA:", movie.get("#AKA", "N/A"))


if __name__ == "__main__":
    movie_title = input("Enter movie title: ")
    get_movie_info(movie_title)
