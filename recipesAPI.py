import requests


# Function to retrieve a recipe suggestion based on ingredients supplied by the user
def retrieve_data():
    url = "https://edamam-recipe-search.p.rapidapi.com/search"

    querystring = {"q": "tomatoes%2C pasta", "health": "vegetarian"}

    headers = {
        'x-rapidapi-host': "edamam-recipe-search.p.rapidapi.com",
        'x-rapidapi-key': "7cde3de9cdmsh9a6cc06496caa69p157663jsnb2febb25651a"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    recipes_data = response.json()

    hits = recipes_data["hits"]

    # go though the data to find the names of suggested recipes which are stored under "label"
    for hit in hits:
        print(hit["recipe"]["label"])


retrieve_data()