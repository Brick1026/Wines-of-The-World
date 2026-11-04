import json
from pathlib import Path
from tkinter import N
import webbrowser
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.impute import SimpleImputer
import tkinter as tk
import quiz as q

MASTER_WINE_DATA_PATH = Path(__file__).resolve().parent / "Data" / "master_wine_data.json"
PAST_RECOMMENDATIONS_PATH = Path(__file__).resolve().parent / "Data" / "past_recommendations.json"

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
            "with": 15
        }
    }
    
    # assigned when sample matrix is built, contains all of the wines
    # in the JSON file as a python array
    wines = None

    # reads a JSON file and converts the values to my internal format
    # param - the answers, we need to know what grapes they liked
    # param - the target file to use to build the sample matrix
    # return - np array where each master_wine_json sample has its attributes
    #          assigned numeric values. 2D array and each sample is a row.
    def build_sample_matrix(self,answers,target):
        arr_samples = []
        # unpack JSON and begin building data matrix
        with target.open("r", encoding="utf-8") as file:
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
    def build_user_sample(self,answers):
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
        _, indices = neighbors.kneighbors(user_imputed)
        return indices
    
    # param - recommendation indices from get_indices_of_recommendations
    # param - the sample matrix used to run nearest neighbors prior
    # param - the answers from the user survey
    # return - the index of the best recommendation
    def most_similar_to_past_recommendations(self,rec_indices,sample_matrix,answers):
        
        # read in my past recommendations 
        past_recommendations = None
        with PAST_RECOMMENDATIONS_PATH.open("r", encoding="utf-8") as file:
            past_recommendations = json.load(file)
        rec_samples = self.build_sample_matrix(answers,PAST_RECOMMENDATIONS_PATH)
        ct = np.shape(rec_samples)[0]
        
        # behavior depends on the number of saved past recommendations
        if ct == 1:
            # put my recommendation samples into a new list
            # using the recommendation indices
            # they are already imputered
            samples = []
            for idx in rec_indices:
                samples.append(sample_matrix[idx][:])
            
            samples = np.asarray(samples)
            
            neighbors = NearestNeighbors(n_neighbors=1,
                                        algorithm="ball_tree").fit(samples)
            
            # impute the recommendation sample
            imputer = SimpleImputer(strategy='mean')
            recs_imputed = imputer.transform(rec_samples)
            
            _, indices = neighbors.kneighbors(recs_imputed[0][:])
            
            if past_recommendations[0]['rating'] > 3:
                return indices[0]
            elif past_recommendations[0]['rating'] < 3:
                return indices[np.size(indices)-1]
            else:
                return rec_indices[0]
            
        elif ct == 2:
            # TODO
            print("todo")
        else:
            # TODO
            print("todo")
            
    
    # param - index of a wine
    # return - the wine at that index
    def get(self,index):
        return self.wines[index]
        
    # Save recommendation with user rating
    # param - answers list containing a single user rating of a recommendation
    # param - survey answers
    def save_recommendation(self,top,params):
        rating, wine = params
        recommendation = {**wine, "rating": rating}

        # JSON tedium
        if PAST_RECOMMENDATIONS_PATH.exists():
            with PAST_RECOMMENDATIONS_PATH.open("r", encoding="utf-8") as file:
                contents = file.read()
            if not contents.strip():
                existing_data = []
            else:
                existing_data = json.loads(contents)
                if isinstance(existing_data, dict):
                    existing_data = (
                        [existing_data]
                        if "wine" in existing_data
                        else list(existing_data.values())
                    )
                if not isinstance(existing_data, list) or not all(
                    isinstance(item, dict) for item in existing_data
                ):
                    raise ValueError("Past recommendations must be a JSON list of wine records")
        else:
            existing_data = []

        # make sure we don't have two rating for the same wine
        for wine in existing_data:
            if wine["wine"] == recommendation["wine"]:
                wine["rating"] = recommendation["rating"]
                break
        else:
            existing_data.append(recommendation)
                
        # write-back
        with PAST_RECOMMENDATIONS_PATH.open("w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
        
        top.destroy()
        top.update()
        
    # Creates a top level recommendation window
    # param - root window
    # param - survey answers
    def get_recommend_window(self,root,params):
        # run learning algo
        user_sample = self.build_user_sample(params)
        samples = self.build_sample_matrix(params,MASTER_WINE_DATA_PATH)
        recommendations = self.get_indices_of_recommendations(user_sample,samples)

        # open browser searching for the recommended wine
        final = self.most_similar_to_past_recommendations(recommendations,params)
        final_entry = self.get(final)
        query = "Wine: " + final_entry["wine"] + " from " + final_entry["country_name"] + " " + final_entry["region_name"]
        webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
        
        # build the recommendation window
        rec_window = tk.Toplevel()
        rec_window.geometry("400x150")
        rec_window.title("Recommendation")
        rec_window.grid_propagate(False)
        rec_window.grid_columnconfigure(0, weight=1)
        
        # make a quiz with a single question
        rating_quiz = q.quiz(rec_window)
        
        # passing the empty list for gui objects because we don't want these to resize
        rating = rating_quiz.make_mult_choice_question(
                            (.013,.01,.01,.01,.01,.01,.01),                
                            "How would you rate this recommendation?",     
                            (["Awful",1],
                                ["Bad",2],
                                ["Ok",3],
                                ["Great",4],
                                ["Amazing",5]),
                            [])    
        rating_quiz.make_submit_button(.013,
                                    "Submit",
                                    (rating,final_entry),[],
                                    self.save_recommendation,rec_window,False)   
    
    # Resets the past_recommendations JSON file 
    def reset(self):  
        PAST_RECOMMENDATIONS_PATH.open('w', encoding="utf-8",).close()
            