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

    # reads a JSON file and converts the values to my internal format
    # param - the answers, we need to know what grapes they liked
    # param - the target file to use to build the sample matrix
    # return - np array where each master_wine_json sample has its attributes
    #          assigned numeric values. 2D array and each sample is a row.
    #
    
    def build_sample_matrix(self,answers,target):
        arr_samples = []
        # unpack JSON and begin building data matrix
        with target.open("r", encoding="utf-8") as file:
            wines = json.load(file)
            
            # only update sample matrix for the object if this is init
            if target == MASTER_WINE_DATA_PATH:
                self.wines = wines
                
            for wine in wines:
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
        grape_preference = self.get_value("liked_grapes","with")
        if (len(answers[6]) == 0):
            grape_preference = self.get_value("liked_grapes","without")
            
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
    # param - the imputer created from the sample matrix
    # return - the recommendation indices ordered from best to worst
    def get_indices_of_recommendations(self,user_sample,samples):
        imputer = SimpleImputer(strategy='mean')
        user_sample = user_sample.reshape(1, -1)
        samples_imputed = imputer.fit_transform(samples)
        user_imputed = imputer.transform(user_sample)
        neighbors = NearestNeighbors(n_neighbors=5,algorithm="ball_tree").fit(samples_imputed)
        _, indices = neighbors.kneighbors(user_imputed)
        return indices[0], imputer
    
    # param - recommendation indices from get_indices_of_recommendations
    # param - the sample matrix used to run nearest neighbors prior
    # param - the answers from the user survey
    # param - the imputer used to fit the sample matrix
    # return - the index of the best recommendation
    def most_similar_to_past_recommendations(self,rec_indices,sample_matrix,answers,imputer):
        
        # read in my past recommendations (to get the rating)
        past_recommendations = None
        with PAST_RECOMMENDATIONS_PATH.open("r", encoding="utf-8") as file:
            contents = file.read()
            if not contents.strip():
                return rec_indices[0]
            past_recommendations = json.loads(contents)
               
        # build a sample matrix in my code's expected format
        past_samples = self.build_sample_matrix(answers,PAST_RECOMMENDATIONS_PATH)
        ct = np.shape(past_samples)[0]
        # make 2D
        past_samples = np.atleast_2d(past_samples)
        
        # impute past samples
        past_samples = imputer.transform(past_samples)
        
        # put my recommendation samples into a new list
        # using the recommendation indices
        # they are already imputered
        rec_samples = []
        for idx in rec_indices:
            rec_samples.append(sample_matrix[idx][:])
        
        rec_samples = np.asarray(rec_samples)
        # make 2D
        rec_samples = np.atleast_2d(rec_samples)
        # impute rec samples
        rec_samples = imputer.transform(rec_samples)
                     
        # behavior depends on the number of saved past recommendations
        if ct == 1:
            
            # buld a nearest neighbors using current recommendations
            neighbors = NearestNeighbors(n_neighbors=len(rec_samples),
                                        algorithm="ball_tree").fit(rec_samples)
            
            
            # Fit the singular past recommendation
            _, indices = neighbors.kneighbors(past_samples)
            indices = indices[0]
            
            # if our past recommendation was good than prioritize the most similar current recommendation
            # to this past recommendation
            if past_recommendations[0]['rating'] > 3:
                candidate_position = int(indices[0])
                master_index = int(rec_indices[candidate_position])
                return master_index
            
            # if our past recommendation was bad than prioritize the least similar current recommendation
            # to this past recommendation
            elif past_recommendations[0]['rating'] < 3:
                candidate_position = int(indices[np.size(indices)-1])
                master_index = int(rec_indices[candidate_position])
                return master_index
            # If the past recommendation was just okay then we can simply return the best we found before
            else:
                return rec_indices[0]
            
        elif ct == 2:
            # build a nearest neighbors using past recommendations
            neighbors = NearestNeighbors(n_neighbors=2,
                                        algorithm="ball_tree").fit(past_samples)
            
            # list because may save muiltiple in case of tie
            best_ratings = [0]
            # indices corrospond to best_ratings list
            indices_of_best_recommendations = []
            tie = False
            for index,sample in enumerate(rec_samples):
                 # Fit the singular past recommendation
                _, indices = neighbors.kneighbors(np.atleast_2d(sample))
                indices = indices[0]
                this_rating = past_recommendations[indices[0]]['rating']
                if(this_rating > best_ratings[0]):
                    # clear lists
                    tie = False
                    best_ratings = []
                    indices_of_best_recommendations = []
                    # Save the index of this sample and its rating
                    indices_of_best_recommendations.append(index)
                    best_ratings.append(this_rating)
                elif(this_rating == best_ratings[0]):
                    tie = True
                    indices_of_best_recommendations.append(index)
                    best_ratings.append(this_rating)
                else: 
                    continue
            # if we have a tie figure out the best of the tie elements
            if(tie):
                # return the rec_idx which appears first in rec_indices
                # AKA the best attribute as defined by the previous step that is 
                # ALSO in the tie
                best_position = np.min(indices_of_best_recommendations)
                return rec_indices[best_position]
            else:
                # only one element to return
                # map back to master wine data array
                return rec_indices[indices_of_best_recommendations[0]]
        else:
            # build a nearest neighbors using past recommendations
            neighbors = NearestNeighbors(n_neighbors=2,
                                        algorithm="ball_tree").fit(past_samples)
            
            sample_weights = []
            for index,sample in enumerate(rec_samples):
                # Fit the singular past recommendation
                _, indices = neighbors.kneighbors(np.atleast_2d(sample))
                indices = indices[0]
                
                # add the sum of the two nearest neighbor's weights
                sample_weights.append(past_recommendations[indices[0]]['rating'] + 
                                      past_recommendations[indices[1]]['rating'])
            
            # convert to np array
            sample_weights = np.array(sample_weights)
            max_val = sample_weights.max()
            indices_of_best_recommendations = np.where(sample_weights == max_val)[0]
            
            # see if we tied
            tie = True if len(indices_of_best_recommendations) > 1 else False
            
            # if we have a tie figure out the best of the tie elements
            if(tie):
                # return the rec_idx which appears first in rec_indices
                # AKA the best attribute as defined by the previous step that is 
                # ALSO in the tie
                best_position = np.min(indices_of_best_recommendations)
                return rec_indices[best_position]
            else:
                # only one element to return
                # map back to master wine data array
                return rec_indices[indices_of_best_recommendations[0]]
            
    
    # param - index of a wine
    # return - the wine at that index
    def get(self,index):
        return self.wines[index]
        
    # param - index of a wine
    def remove(self,index):
        del self.wines[index]
    
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
        recommendations,imputer = self.get_indices_of_recommendations(user_sample,samples)

        # open browser searching for the recommended wine
        final = self.most_similar_to_past_recommendations(recommendations,samples,params,imputer)
        final_entry = self.get(final)

        
        query = "Wine: " + final_entry["wine"] + " from " + final_entry["country_name"] + " " + final_entry["region_name"]
        webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
        
        # remove this recommendation from the master wine data file so that we avoid double recommendations
        data = None
        with MASTER_WINE_DATA_PATH.open("r", encoding="utf-8") as file:
            contents = file.read()
            if not contents.strip():
                data = []
            else:
                data = json.loads(contents)   
        del data[final]
        with MASTER_WINE_DATA_PATH.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
                    
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
            