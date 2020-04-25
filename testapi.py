import requests


def retrieve_data(value):

    URL1 = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

    querystring = {"number": "5", "ranking": "1", "ignorePantry": "false", "ingredients": value}

    headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': "51d5225cf3msh3beb5dacf075161p1812b2jsnba32bca5162d",
    }

    response1 = requests.request("GET", URL1, headers=headers, params=querystring)

    recipes_data = response1.json()

    titles = []
    ids = []
    recipe_fat_list = []
    recipe_protein_list = []
    recipe_carbs_list = []

    for hit in recipes_data:
        titles.append(hit["title"])
        ids.append(hit["id"])

    links = []
    keys = ["fat", "carbs", "protein"]

    for id in ids:
        URL2 = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/" + str(id) + "/information"
        response2 = requests.request("GET", URL2, headers=headers, params=querystring)
        other_data = response2.json()
        links.append(other_data["sourceUrl"])

    for id in ids:
        URL3 = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/" + str(id) + "/nutritionWidget.json"
        response3 = requests.request("GET", URL3, headers=headers, params=querystring)
        response3_json = response3.json()

        #print(response3_json)

        for key in keys:
            if key == "fat":
                response_fat_no_units = response3_json[key][:-1]
                recipe_fat_list.append(response_fat_no_units)
            elif key == "carbs":
                response_carbs_no_units = response3_json[key][:-1]
                recipe_carbs_list.append(response_carbs_no_units)
            elif key == "protein":
                response_protein_no_units = response3_json[key][:-1]
                recipe_protein_list.append(response_protein_no_units)

    return [titles, links, recipe_fat_list, recipe_carbs_list, recipe_protein_list]





