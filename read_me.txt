This application is a program designed to curate wines for you based on an initial survey.
There is a element of randomness to the decision algorithm to allow for unique results on repeat usage.
Based on your response to the recommendations the algorithm is further adjusted 
to filter the results of your search on subsequent usage.

Files:

main.py - Main program spinup and setup tkinter
user_profile.csv - Location saving the user's selection to preference prompts
past_recommendations.csv - Location saving past recommendations and how the user rated them
master_wine_data.json - Holds the result of the massive query on program start

Wine Learning Algorithm Attributes:

    Nearest Neighbors Attributes:
        "wine": "Les Valnons Brut Nature Champagne Grand Cru 'A\u00ff'",
        "type": "Sparkling",
        "acidity": "High",
        "abv": "12.2",
        "country_name": "France",
        "body": "Medium-bodied",
        "winery_name": "Roger Pouillon & Fils",
        "region_name": "Champagne",


Process:

    1. User is asked to provide their preferences on a variety of wine characteristics.
            - At each question the user is asked to rate on a scale of 1/10 how important that aspect is to them.
            - Some of these questions are fill in the blank, some will be multiple choice, and
                some will be true or false.

    2. The user is asked how much they want the program to think about it's answer. Based on this, the program
        will decide how many iterations of nearest neighbors to perform to build its set of answers.

        Every value in the set of answers is initialized with a weight of 1.0.

    3. Each element of this subset is then compared to all past_recommendations to identify similarities.
       Based on the rating of past recommendations this 

    

    


    
        

