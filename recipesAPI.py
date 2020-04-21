import requests
import numpy as np


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

    # Go though the data to find the names of suggested recipes which are stored under "label"
    for hit in hits:
        recipe_names_list.append(hit["recipe"]["label"])
        recipe_names_list.append(hit["recipe"]["url"])

    recipe_fat_list = []
    recipe_sugar_list = []
    recipe_protein_list = []
    recipe_fiber_list = []

    for hit in hits:
        keys = ["FAT", "SUGAR","PROCNT", "FIBTG"]

        for key in keys:
            if key == "FAT":
                recipe_fat_list.append(hit["recipe"]["totalNutrients"][key]["quantity"])
            elif key == "SUGAR":
                recipe_sugar_list.append(hit["recipe"]["totalNutrients"][key]["quantity"])
            elif key == "PROCNT":
                recipe_protein_list.append(hit["recipe"]["totalNutrients"][key]["quantity"])
            elif key == "FIBTG":
                recipe_fiber_list.append(hit["recipe"]["totalNutrients"][key]["quantity"])

    formatted_recipe_fat_list = list(np.around(np.array(recipe_fat_list), 2))
    formatted_recipe_sugar_list = list(np.around(np.array(recipe_sugar_list), 2))
    formatted_recipe_protein_list = list(np.around(np.array(recipe_protein_list), 2))
    formatted_recipe_fiber_list = list(np.around(np.array(recipe_fiber_list), 2))

    return [recipe_names_list, formatted_recipe_fat_list, formatted_recipe_sugar_list, formatted_recipe_protein_list, formatted_recipe_fiber_list]


def retrieve_data_Spoonacular(input_value):

    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

    querystring = {"number": "5", "ranking": "1", "ignorePantry": "false", "ingredients": input_value}

    headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': "51d5225cf3msh3beb5dacf075161p1812b2jsnba32bca5162d"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)


if __name__ == "__main__":
    retrieve_data_Edamam("apples, sugar")
