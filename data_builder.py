# Class to take master_wine_data.json and 
# using the survey answers convert the qualitative data
# into quantitative data the learning algo can understand.
class data_builder:
    
    # param - survey results as a tuple of quesion answers
    # return - array where each master_wine_json sample has its attributes
    #          assigned numeric values
    def build_sample_matrix(survey_results):
        