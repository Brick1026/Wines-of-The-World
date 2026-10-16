This application is a program designed to curate wines for you based on an initial survey.
There is a element of randomness to the decision algorithm to allow for unique results on repeat usage.
Based on your response to the recommendations the algorithm is further adjusted 
to filter the results of your search on subsequent usage.

Files:

main.py - Main program spinup and setup tkinter
past_recommendations.json - Location saving past recommendations and how the user rated them
master_wine_data.json - Holds the result of the massive query on program start

Wine Learning Algorithm Attributes:

    Nearest Neighbors Attributes:
        "wine"
        "grapes"
        "sweetness"
        "type"
        "acidity"
        "abv"
        "country_name"
        "body"
        "winery_name"
        "region_name"

Process:

    1. A query runs which grabs some number of wine entries from an open API.
    
    2. Threads randomly select wines to add to this sessions "master_wine_data.json"

    3. 
    1. User is asked to provide their preferences on a variety of wine characteristics.

    2. The user is asked how much they want the program to think about it's answer. Based on this, the program
        will decide how many iterations of nearest neighbors to perform to build its set of answers.

    3. Each element of this subset is then compared to all past_recommendations to identify similarities.

    4. A recommendation is made.

    5. User rates recommendation

    

    


    
        

