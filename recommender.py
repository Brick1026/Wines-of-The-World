import numpy as np

# Class to take master_wine_data.json and 
# using the survey answers convert the qualitative data
# into quantitative data the learning algo can understand.
class recommender:
    
    # param - survey results as a tuple of quesion answers
    # return - np array where each master_wine_json sample has its attributes
    #          assigned numeric values. 2D array and each sample is a row.
    @staticmethod
    def build_sample_matrix(answers):
        print("TODO")
       
    # param - survey results as a tuple of quesion answers
    # return - 2D NP array with one row representing the user 
    #          sample
    @staticmethod
    def build_user_sample(answers):
        print("TODO")