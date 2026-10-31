This application is a program designed to curate wines for you based on an initial survey.
There is an element of randomness to the decision algorithm to allow for unique results on repeat usage.*
Based on your response to the recommendations the algorithm is further adjusted 
to filter the results of your search on subsequent usage.

*Every run a new random set of wines are grabbed from a public database of wines which allows for new recommendations

Important Definitions for Non-CS people
words found here are denoted with a ^ symbol next to them:

Thread - A thread is a singular logical processor. Modern computers contain multiple processors. 
Threaded programs leverage more than one of these processors to work on things simultaneously.
This is like doing two loads of laundry at the same time by having one in the dryer and one in the washer
as opposed to 




Files:

main.py - Main program spin up and setup tkinter 
load.py - Loading screen visual and starts fetch
fetch.py - Queries and compiles data into my attribute format. Uses threads to speed up process.
quiz.py - Class for easily creating tkinter quiz

past_recommendations.json - Location saving past recommendations and how the user rated them
master_wine_data.json - Holds the result of the massive query on program start

Wine Learning Algorithm Attributes:

    Nearest Neighbors Attributes:
       "type"
       "acidity"
       "sweetness"
       "abv"
       "body"
       "world"
       "liked_grapes"

Process:

    1. Query runs which grabs wines from a wine database to build a catalog of wines

    2. Threads^ randomly select wines from the catalog and build JSON elements
    using the attributes as is or conditional logic to create new attributes.
        Ex: Sweetness is not an attribute in the database, so the threads look for
        sweetness keywords in the names of wines.
    
    3. Main run loop and window spins up presenting the user a survey to assess their preferences.

    4. 



    

    


    
        

