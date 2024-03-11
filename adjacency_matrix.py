#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 15:56:46 2023

@author: medhabulumulla

Making an Adjacency Matrix
"""

import pandas as pd
import numpy as np 
import itertools

plants = pd.read_csv(r'/Users/medhabulumulla/Desktop/INFO_5311/plants-and-cooking/plant-clean.csv')
# small UK -> US terminology; bell pepper -> capsicum, fava bean -> broad bean
# Brassicas describes cabbage, collard greens, brocolli, brussel sprouts, kale
brassica_plants = ['cabbage', 'collard', 'brocolli', 'brussels_sprout', 'kale']
allium_plants = ['onion', 'garlic', 'leek', 'shallot', 'chive']

# function that cleans the plant data, replaces spaces, fixes spelling errors, makes lower, etc. 
def cleanPlants(data):
    newdata = []
    for idx, plant in enumerate(data):
        if(pd.isnull(plant)): newdata.append(plant)
        else:
            if(plant[len(plant)-1:len(plant)] == "_"): plant= plant[0:len(plant)-1]
            if(plant[len(plant)-1:len(plant)] == "s" and plant.lower() not in ["asparagus", "cress"]): plant= plant[0:len(plant)-1]
            if(plant == "camomile"): plant = "chamomile"
            newdata.append(plant.lower().replace(" ", "_").replace("-", "").replace(".", "") )
    return newdata


plant_names_cols =  ['name1','compat1', 'compat2', 'compat3',
'compat4', 'compat5', 'compat6', 'compat7', 'compat8', 'compat9',
'compat10', 'compat11']

plant_names_full_cols =  ['name1', 'name2', 'name3', 'name4', 'name5','compat1', 'compat2', 'compat3',
'compat4', 'compat5', 'compat6', 'compat7', 'compat8', 'compat9',
'compat10', 'compat11']

for col in plant_names_full_cols: 
    plants[col] = cleanPlants(plants[col] ) 


# making a list of ALL plants
plant_lists = [plants[col] for col in plant_names_cols ]
all_plants = [plant for plant in list(itertools.chain.from_iterable(plant_lists)) if str(plant) != 'nan']
all_plants_unique = np.unique(all_plants).tolist() 


# # making the adjaceny matrix
# adj_matrix = []
# for i in range(0,113): adj_matrix.append([0]*112)
# adj_df = pd.DataFrame(adj_matrix, columns = all_plants_unique)

# for i in range(0,92): # iterate thru plants' rows
#     compPlants = [plants['compat' + str(c)][i] for c in range(1,11) ]
#     compPlants = [plant.lower().replace(" ", "_").replace("-", "").replace(".", "") for plant in compPlants if str(plant) != 'nan']
#     # print(plants['name1'][i], ":", compPlants)
#     ## Handle plant families
#     if ('brassica' in compPlants ):
#         compPlants.extend(brassica_plants)
#         # print(plants['name1'][i], ":", compPlants)
#     if ('allium' in compPlants):
#         compPlants.extend(allium_plants) 
#     for col in adj_df.columns: # iterate thru 116 columns to see if there's a match
#         if(col in compPlants):   
#             adj_df[col][i] = 1
#             # print(plants['name1'][i], ":", col)
   

# # adj_df.to_json('adj_matrix.json', orient="split")        
# # adj_df.to_csv('adj_matrix.csv', index = False)
    
# # SUBSETTING DATASET

# connect_nums = []
# remove_cols = []
# keep_cols = []
# remove_rows = []
# keep_rows = []
# for i in range(len(adj_df)):
#     sum_val = adj_df.iloc[i].sum()
#     connect_nums.append(sum_val)
#     if (sum_val >= 7):
#         keep_cols.append(adj_df.columns[i])
#         keep_rows.append(i)
#     else:
#         remove_cols.append(adj_df.columns[i])
#         remove_rows.append(i)

# connections = pd.DataFrame({"nodes": adj_df.columns,"edges": connect_nums})
# connections = connections.sort_values('edges').reset_index(drop = True)
# # connections.to_csv('connections.csv', index = False)

# adj_df_subset = adj_df.drop(columns=remove_cols, index = remove_rows).reset_index(drop = True)
# # adj_df_subset.to_json('adj_matrix_subset.json', orient="split")        
# # adj_df_subset.to_csv('adj_matrix_subset.csv', index = False)




# [1]*31
# nodes = pd.DataFrame({ "weight": [1]*len(keep_cols), "name": keep_cols, "plant-family":["plant"]*len(keep_cols)})
# # nodes.to_json('nodes_records.json',orient='records')
# # nodes.to_json('nodes_split.json',orient='split')


# # make edges
# # edges = pd.DataFrame({"source": , "target", "sourceIndex":, "targetIndex":, "weight":})


# #%%
# sources = []
# targets = []
# srcidxs = []
# tgtidxs = []


# for srcIdx, srcCol  in enumerate(keep_cols): 
#     for tgtIdx, tgtCol in enumerate(keep_cols): 
#         if( adj_df_subset.iloc[[srcIdx]][tgtCol][srcIdx] == 1):
#             sources.append(srcCol)
#             targets.append(tgtCol)
#             srcidxs.append(srcIdx)
#             tgtidxs.append(tgtIdx)
            
# # edges = pd.DataFrame({"source": sources, "target": targets, "sourceIndex": srcidxs, "targetIndex":tgtidxs})
# # edges.to_json('edges_records.json',orient='records')

# #%%  



#%%
ingredients = pd.read_csv(r'/Users/medhabulumulla/Desktop/INFO_5311/plants-and-cooking/raw-data/medha-data/ingredient-list.csv')
ingredients = pd.read_csv(r'/Users/medhabulumulla/Desktop/INFO_5311/plants-and-cooking/raw-data/recipe-original.csv')

# ingredients['ingredient-list'][0].split()
ingredients_removed = []
intersect_sets = []
intersect_nums = []
all_plants_unique.append("spring_onions")

for i in range(0, 13501):
    # ingreList = ingredients['ingredientList'][i].replace("'", "").replace(",", "")
    ingreList = ingredients['Cleaned_Ingredients'][i].replace("'", "").replace(",", "")
    ingre_list = ingreList.split()
    intersect_set = set(ingre_list).intersection(all_plants_unique)
    intersect_num = len(intersect_set)
    if(intersect_num > 0):
        # recipe_indices.append(i)
        # print(ingredients['Title'][i], intersect_set)
        intersect_sets.append(intersect_set)
        intersect_nums.append(intersect_num)
    else: 
        ingredients_removed.append(i)

ingredients_subset = ingredients.drop(index = ingredients_removed).reset_index(drop = True)
ingredients_subset['cropListOrig'] = intersect_sets
ingredients_subset['cropNum'] = intersect_nums

ingredients_subset['cropList'] = [str(cr).replace('}', '').replace('{', '').replace('\'', '') for cr in ingredients_subset['cropListOrig']]

ingredients_subset.to_csv('ingredients-and-crops.csv', index = False)

#%%
