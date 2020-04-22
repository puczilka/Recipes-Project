import requests
import json
import numpy as np
from collections import Counter
#=========================================put in function when you know how the input is formatted from DASH=======================
# cuisines to exclude
cuisine_excl=[ "american", "african" ,"british" , "cajun" , "caribbean" , "chinese" , "eastern european" , "european" , "french",
               "german" , "greek" , "indian" , "irish" , "japanese" , "jewish" , "korean" , "latin american" , "mediterranean" ,
               "mexican" , "middle eastern" , "nordic" , "southern" , "spanish", "thai", "vietnamese"]


# all cuisines available
cuisine_total = "african , american , british , cajun , caribbean , chinese , eastern european , european , french, " \
                "german , greek , indian , irish , italian , japanese , jewish , korean , latin american , mediterranean , " \
                "mexican , middle eastern , nordic , southern , spanish , thai , vietnamese  "

# eliminate the cuisines (chosen by user) in cuisine total
#cuisine total is an input to the function get_recipes
for i in range(len(cuisine_excl)):
    if cuisine_excl[i] == "vietnamese":
        cuisine_total = cuisine_total.replace(cuisine_excl[i], " ")
    else:
        cuisine_total = cuisine_total.replace((cuisine_excl[i] + " ,"), " ")

    #print((cuisine_excl[i]))

print(cuisine_total)

#===================================end function for formatting/ inputting the cuisine================================

#===================================start ingredients input===========================================================

ingredients="pasta, tomatoes, onion, cheese, mushroom, pepper, chicken "

ingredients_in= ingredients.replace(",", "%2C")

print(ingredients, ingredients_in)
#===================================end function for formatting/ inputting the cuisine================================

def get_recipes(cuisine_in, ingredients):
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/searchComplex"

    #querystring = {"includeIngredients":"onions%2Clettuce%2Ctomato","instructionsRequired":"true", "addRecipeInformation":"false","ranking":"1",
    #               "sort":"max-used-ingredients","sortDirection": "desc","limitLicense":"false","offset":"0","number":"50"}

    #querystring = {"query":"burger","cuisine":"american","includeIngredients":"onions%2C lettuce%2C tomato","excludeIngredients":"coconut%2C mango","intolerances":"peanut%2C shellfish","type":"main course","ranking":"2","minCalories":"150","maxCalories":"1500","minFat":"5","maxFat":"100","minProtein":"5","maxProtein":"100","minCarbs":"5","maxCarbs":"100","minAlcohol":"0","maxAlcohol":"1000","minCaffeine":"0","maxCaffeine":"1000","minCopper":"0","maxCopper":"1000","minCalcium":"0","maxCalcium":"1000","minCholine":"0","maxCholine":"1000","minCholesterol":"0","maxCholesterol":"1000","minFluoride":"0","maxFluoride":"1000","minSaturatedFat":"0","maxSaturatedFat":"50","minVitaminA":"0","maxVitaminA":"5000","minVitaminC":"0","maxVitaminC":"1000","minVitaminD":"0","maxVitaminD":"1000","minVitaminE":"0","maxVitaminE":"1000","minVitaminK":"0","maxVitaminK":"1000","minVitaminB1":"0","maxVitaminB1":"1000","minVitaminB2":"0","maxVitaminB2":"1000","minVitaminB3":"0","maxVitaminB3":"1000","minVitaminB5":"0","maxVitaminB5":"1000","minVitaminB6":"0","maxVitaminB6":"1000","minVitaminB12":"0","maxVitaminB12":"1000","minFiber":"0","maxFiber":"1000","minFolate":"0","maxFolate":"1000","minFolicAcid":"0","maxFolicAcid":"1000","minIodine":"0","maxIodine":"1000","minIron":"0","maxIron":"1000","minMagnesium":"0","maxMagnesium":"1000","minManganese":"0","maxManganese":"1000","minPhosphorus":"0","maxPhosphorus":"1000","minPotassium":"0","maxPotassium":"1000","minSelenium":"0","maxSelenium":"1000","minSodium":"0","maxSodium":"1000","minSugar":"0","maxSugar":"1000","minZinc":"0","maxZinc":"1000","equipment":"pan","limitLicense":"false","offset":"0","number":"10"}


    #print(cuisine_total)

    #querystring = {"cuisine":"italian, american, british, cajun, caribbean","includeIngredients":"onions%2C lettuce%2C tomato","addRecipeInformation":"true","ignorePantry":"false","limitLicense":"false","offset":"0","number":"5"}

    querystring = {"cuisine": cuisine_in,
                   "includeIngredients": ingredients, "addRecipeInformation": "true",
                   "sort":"popularity",
                   "ignorePantry": "false", "limitLicense": "false", "offset": "0", "number": "100"}

    #querystring = {"query":"burger","cuisine":"american","number":"10"}


    headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': "51d5225cf3msh3beb5dacf075161p1812b2jsnba32bca5162d"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    options_json=response.json()
    #print(response.text)
    #print(options_json['results'])
    ingredients_tot = []
    title_array=[]
    print("lenght",len(options_json['results']))
    for i in range(len(options_json['results'])):
        id = options_json['results'][i]['id']
        title= options_json['results'][i]['title']
        missed_ingr = options_json['results'][i]['missedIngredientCount']
        used_ingr= options_json['results'][i]['usedIngredientCount']
        cuisines = options_json['results'][i]['cuisines']
        title_array.append(title)
        print(title,missed_ingr, used_ingr, cuisines)

        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/" + str(id) + "/information"
        #print(url)

        response = requests.request("GET", url, headers=headers)
        response_recipe_json = response.json()
        #print(response_recipe_json)
        index=(tuple(b+1 for b in group) for group in response_recipe_json['extendedIngredients'])
        index=tuple( ele   for ele in range(len(response_recipe_json['extendedIngredients'])))

        print(index.index(1), type(index.index(1)))

        ingredients_results=list(map(lambda b: b['name'], response_recipe_json['extendedIngredients']))
        #ingredients_results = map(lambda d: d['extendedIngredients'], response_recipe_json)
        #names = map(lambda d: d['name'], variation_json)

        #print(ingredients_results)


        # ingredients_results = []
        #
        # for i in range(len(response_recipe_json['extendedIngredients'])):
        #
        #     ingredients_results.append(str( response_recipe_json['extendedIngredients'][i]['name']))
        #
        ingredients_tot.append(ingredients_results)
    print(ingredients_tot)
    return ingredients_tot, title_array







def max_ingredients(ingredients_results, ingredients, title_array):
    # using Union operation using set theory you need
    ingredients_user= ingredients.split(",") #change to array
    matches_array=[]
    print(ingredients_user)
    print(len(ingredients_results),len(ingredients_results[1]) )
    intersection_recipe=[]
    intersec_index=[]
    for i in range(len(ingredients_user)):

        completed_ingr= complete_search(ingredients_user[i])
        #intersection_recipe[i]=[]

        #intersection_recipe = list(map(lambda d: d.intersection(completed_ingr), set(ingredients_results)))
        for j in range(len(ingredients_results)):
            print(ingredients_results[j],ingredients_user[i])

            intersection_recipe=list(set(ingredients_results[j]).intersection(set(completed_ingr)))
            if len(intersection_recipe) != 0:
                intersec_index.append(j)

        print(intersec_index)

    #print(list((Counter(intersec_index) - Counter(set(intersec_index))).keys()))
    intersec_dict= dict(Counter(intersec_index))
    print(dict(Counter(intersec_index)))
    #names=list(map(lambda d: d['name'], variation_json))
    #list(map(lambda d: d.value, intersec_index))
    intersec_sort = sorted(intersec_dict.items(), key=lambda x: x[1],reverse=True)
    print(intersec_sort, len(intersec_sort) , type(intersec_sort[0]))
    recipes_array=list(map(lambda d:list(d)[0], intersec_sort ))
    recipes_results=list(map(lambda d:title_array[d], recipes_array))
    print(recipes_results)

    # for i in range(len(ingredients_results)):                       #matrix of ingredients
    #     match=0
    #     for j in range(len(ingredients_user)):                      #input of ingred from user
    #         print(ingredients_results[i],ingredients_user[j], ingredients_results[i].count(ingredients_user[j]) )
    #         match= match + ingredients_results[i].count(ingredients_user[j])
    #     matches_array.append(match)
    #     print(matches_array)




def complete_search(to_complete):
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/ingredients/autocomplete"

    querystring = {"number": "100", "intolerances": "egg", "query": to_complete}

    headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': "51d5225cf3msh3beb5dacf075161p1812b2jsnba32bca5162d"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    variation_json= response.json()
    #print(type(variation_json))
    names=list(map(lambda d: d['name'], variation_json))
    #print(response.text)
    print(names, "--------------------------------------")
    return names

ingredients_results, title_array=get_recipes(cuisine_total, ingredients)
max_ingredients(ingredients_results, ingredients , title_array)
#complete_search("cheese")
