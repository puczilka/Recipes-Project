import requests
import json


# Function to retrieve a recipe suggestion based on ingredients supplied by the user
def retrieve_data_Edamam(input_value):
    value = input_value

    url = "https://edamam-recipe-search.p.rapidapi.com/search"

    querystring = {"q": value, "health": "vegetarian"}

    headers = {
        'x-rapidapi-host': "edamam-recipe-search.p.rapidapi.com",
        'x-rapidapi-key': "7cde3de9cdmsh9a6cc06496caa69p157663jsnb2febb25651a"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    recipes_data = response.json()
    print(response.text)

    hits = recipes_data["hits"]
    recipe_names_list = []

    # go though the data to find the names of suggested recipes which are stored under "label"
    for hit in hits:
        recipe_names_list.append(hit["recipe"]["label"])
        recipe_names_list.append(hit["recipe"]["url"])

    print(recipe_names_list)
    return recipe_names_list


def retrieve_data_Spoonacular(input_value):

    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

    querystring = {"number": "5", "ranking": "1", "ignorePantry": "false", "ingredients": input_value}

    headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': "51d5225cf3msh3beb5dacf075161p1812b2jsnba32bca5162d"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    recipes_data = response.json()


    print(response.text)



if __name__ == "__main__":
    retrieve_data_Edamam("apples, sugar")
