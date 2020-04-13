import requests
import json

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

querystring = {"number":"5","ranking":"1","ignorePantry":"false","ingredients":"apples%2Cflour%2Csugar"}

headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': "51d5225cf3msh3beb5dacf075161p1812b2jsnba32bca5162d"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)


#print(type(response))
print(response.json()[1])
#print(type(response.json()))
response_options_json= response.json()

id=response_options_json[1]['id']
title=response_options_json[1]['title']
missed_ingr= response_options_json[1]['missedIngredientCount']
print(id, title, missed_ingr)

print(type(id))


url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"+ str(id) + "/information"
print(url)



response = requests.request("GET", url, headers=headers)

print(response.text)
response_recipe_json=response.json()
instructions= response_recipe_json['instructions']
print(instructions)