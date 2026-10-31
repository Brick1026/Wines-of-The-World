import json
from pathlib import Path
from tkinter import N
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.impute import SimpleImputer

MASTER_WINE_DATA_PATH = Path(__file__).resolve().parent / "Data" / "master_wine_data.json"

# Class to take master_wine_data.json and 
# using the survey answers convert the qualitative data
# into quantitative data the learning algo can understand.
class recommender:
    
    # holds the integer values of different properties
    # if you want to weight things differently change them here and it will effect the rest
    # of the program
    
    # since this is a nearest neighbors algorithm I tried to put similar
    # attributes nearby (even though not all of these are related)
    # by increasing the value range you can increase the importance of an attribute!
    
    # Translation dictionary from survey labels to their assigned numeric values.
    
    
    value_dict = {
        #important attribute
        "type": {
            "red": 1,
            "white": 2,
            "sparkling": 3,
            "dessert": 4,
            "fortified": 5,
        },
        "acidity": {
            "low": 1,
            "medium": 2,
            "high": 3,
        },
        # very important attribute
        "sweetness": {
            "dry": 1,
            "semi": 5,
            "sweet": 10,
        },
        "abv": {
            "low": 1,
            "medium": 2,
            "high": 3,
        },
        "body": {
            "light-bodied": 1,
            "medium-bodied": 2,
            "full-bodied": 3,
        },
        "world": {
            "old world": 1,
            "new world": 3,
        },
        # very important attribute
        "liked_grapes": {
            "without": 1,
            "with": 10
        }
    }
    
    # assigned when sample matrix is built, contains all of the wines
    # in the JSON file as a python array
    wines = None

    # param - the answers, we need to know what grapes they liked
    # return - np array where each master_wine_json sample has its attributes
    #          assigned numeric values. 2D array and each sample is a row.
    def build_sample_matrix(self,answers):
        arr_samples = []
        # unpack JSON and begin building data matrix
        with MASTER_WINE_DATA_PATH.open("r", encoding="utf-8") as file:
            self.wines = json.load(file)
            for wine in self.wines:
                common_grapes = "without"
                # see if there are common grapes between user preferences and sample
                for grape in wine.get("grapes"):
                    # if a grape is in the list of user grapes, then update to with otherwise
                    # leave common_grapes value intact
                    common_grapes = "with" if grape.lower() in [ans.lower() for ans in answers[6]] else common_grapes
                    
                arr_samples.append(np.array([
                    self.get_value("type",wine.get("type")),
                    self.get_value("acidity",wine.get("acidity")),
                    self.get_value("sweetness",wine.get("sweetness")),
                    self.get_value("abv",wine.get("abv")),
                    self.get_value("body",wine.get("body")),
                    self.get_value("world",wine.get("world")),
                    self.get_value("liked_grapes",common_grapes)
                ]))
        return np.asarray(arr_samples)
       
    # param - survey results as a tuple of question answers
    # return - 2D NP array with one row representing the user 
    #          sample
    def build_user_sample(self, answers):
        # if user gave grape preferences then set to with otherwise without
        grape_preference = self.get_value("liked_grapes","without")
        if (len(answers[6]) == 0):
            grape_preference = self.get_value("liked_grapes","with")
            
        return np.array([answers[0],
                         answers[1],
                         answers[2],
                         answers[3],
                         answers[4],
                         answers[5], grape_preference])
    
    # param - name of the attribute
    # param - name of the attribute value (key)
    # return - the value of the key from the hardcoded dictionary
    def get_value(self, attribute, name):
        if not isinstance(attribute, str) or not isinstance(name, str):
            return None
        return self.value_dict.get(attribute.lower(), {}).get(name.lower())
    
    # param - user_sample
    # param - samples array
    # return - the recommendation indices ordered from best to worst
    def get_indices_of_recommendations(self,user_sample,samples):
        imputer = SimpleImputer(strategy='mean')
        user_sample = user_sample.reshape(1, -1)
        samples_imputed = imputer.fit_transform(samples)
        user_imputed = imputer.transform(user_sample)
        neighbors = NearestNeighbors(n_neighbors=5,algorithm="ball_tree").fit(samples_imputed)
        distances, indices = neighbors.kneighbors(user_imputed)
        return indices
    
    # param - recommendation indices from get_indices_of_recommendations
    # return - the index of the best recommendation
    def most_similar_to_past_recommendations(self,recommendations):
        return int(recommendations[0][0])
    
    # param - index of a wine
    # return - the wine at that index
    def get(self,index):
        return self.wines[index]