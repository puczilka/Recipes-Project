import requests
import json
#from testdash import input_value


def retrieve_data(value):



    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"


    querystring = {"number":"5","ranking":"1","ignorePantry":"false","ingredients":str(value.replace(' ', '%2C'))}

    headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': "51d5225cf3msh3beb5dacf075161p1812b2jsnba32bca5162d"
}

    response = requests.request("GET", url, headers=headers, params=querystring)

    recipes_data = response.json()
    titles = []
    ids = []
    for hit in recipes_data:
        titles.append(hit["title"])
        ids.append(hit["id"])

    links = []
    for id in ids:
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/" + str(id) + "/information"
        response = requests.request("GET", url, headers=headers, params=querystring)
        other_data = response.json()
        links.append(other_data["sourceUrl"])
    return titles, links


#test = retrieve_data()




