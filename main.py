# Main GUI runloop

from genericpath import exists
import json
from pathlib import Path
import tkinter as tk
from tkinter import Listbox, ttk
from fetch import get_grapes
import quiz as q
import recommender as r
from load import load
from PIL import Image, ImageTk
import webbrowser


# list of on screen gui objects
gui_objects = []

recommender = r.recommender()
PAST_RECOMMENDATIONS_PATH = Path(__file__).resolve().parent / "Data" / "past_recommendations.json"

def main():
    
    load()
    root = tk.Tk()
    my_quiz = q.quiz(root)
    
    # defines the next avaliable grid slot used by question
    root.resizable(height = True, width = True)
    root.title("Wine Curator") 
    root.geometry("710x900")
    root.grid_propagate(False)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    
    # decorative panel
    side_panel = tk.Frame(root)
    # populate decorative panel
    img = Image.open("graphics\\Red_Wine.png")
    img = img.resize((300, 500), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(side_panel,image=photo)
    
    # page title
    title = tk.Label(
                root,
                text="Wines of The World",
                font=("Arial", 24, "bold"),
                anchor="center",
                bg="#2B2B2B",
                fg="#F2F2F2",
                padx=12,
                pady=12,
            )
    
    # define the overall page layout
    title.grid(row=0, column=0, columnspan=2, sticky="ew")
    side_panel.grid(row=1, column=1, sticky="nsew",padx=10,pady=10)
    
    # have to declare even if not using
    img_label._font_scale = 0 
    img_label.pack(fill="both", expand=True)
    gui_objects.append(img_label)
    
    type_preference = my_quiz.make_mult_choice_question(
                        (.013,.01,.01,.01,.01,.01,.01),                
                        "What is your preferred wine type?",     
                        (["Fortified",recommender.get_value("type", "fortified")],
                         ["Red",recommender.get_value("type", "red")],
                         ["White",recommender.get_value("type", "white")],
                         ["Sparkling",recommender.get_value("type", "sparkling")],
                         ["Dessert",recommender.get_value("type", "dessert")]),
                        gui_objects)                     
    
    acid_preference = my_quiz.make_mult_choice_question(
                        (.013,.01,.01,.01,.01),                
                        "What is your preferred wine acidity?", 
                        (["Low",recommender.get_value("acidity", "low")],
                         ["Medium",recommender.get_value("acidity", "medium")],
                         ["High",recommender.get_value("acidity", "high")]),
                        gui_objects)  
    
    sweetness_preference = my_quiz.make_mult_choice_question(
                            (.013,.01,.01,.01,.01),                
                            "What is your preferred wine sweetness?", 
                            (["Dry",recommender.get_value("sweetness", "dry")],
                             ["Semi",recommender.get_value("sweetness", "semi")],
                             ["Sweet",recommender.get_value("sweetness", "sweet")]),
                            gui_objects)        
                                                
    abv_preference = my_quiz.make_mult_choice_question(
                        (.013,.01,.01,.01,.01),                
                        "What is your preferred abv?", 
                        (["Low (0-12.5%)",recommender.get_value("abv", "low")],
                         ["Medium (12.5-13.5%)",recommender.get_value("abv", "medium")],
                         ["High (13.5%+)",recommender.get_value("abv", "high")]),
                        gui_objects)    
        
    body_preference = my_quiz.make_mult_choice_question(
                        (.013,.01,.01,.01,.01),                
                        "What is your preferred wine body?", 
                        (["Light",recommender.get_value("body", "light-bodied")],
                         ["Medium",recommender.get_value("body", "medium-bodied")],
                         ["Full",recommender.get_value("body", "full-bodied")]),
                        gui_objects)    
    
    
    world_preference = my_quiz.make_mult_choice_question(
                        (.013,.01,.01,.01),                
                        "Do you prefer old world or new world wine?", 
                        (["Old World",recommender.get_value("world", "old world")],
                         ["New World",recommender.get_value("world", "new world")]),
                        gui_objects)    
    
    # add grape preference question
    query_grapes = get_grapes()
    query_array = sorted(query_grapes.items(), key=lambda item: item[0].casefold())
    grape_preference = my_quiz.make_mult_select_question(
                        (.013,.01,.01),
                        "Choose your favorite of these grapes!",
                        query_array,
                        gui_objects)

    answers = (type_preference,
            acid_preference,
            sweetness_preference,
            abv_preference,
            body_preference,
            world_preference,
            grape_preference)

    my_quiz.make_submit_button(.013,
                               "Recommend me!",
                               answers,gui_objects,
                               get_recommend_window,root)
    
    # configure the lambda event to call resize on configure
    root.bind("<Configure>", lambda event: resize(event, root, side_panel))
    root.after_idle(lambda: resize(None, root, side_panel))
    root.mainloop()

# Creates a top level recommendation window
# param - root window
# param - survey answers
def get_recommend_window(root,params):
    # run learning algo
    user_sample = recommender.build_user_sample(params)
    samples = recommender.build_sample_matrix(params)
    recommendations = recommender.get_indices_of_recommendations(user_sample,samples)

    # open browser searching for the recommended wine
    final = recommender.most_similar_to_past_recommendations(recommendations)
    final_entry = recommender.get(final)
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
                                   save_recommendation,rec_window)     
    
# Save recommendation with user rating
# param - answers list containing a single user rating of a recommendation
# param - survey answers
def save_recommendation(top,params):
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
    
# Resizes all widgets in GUI
# param - The triggering event
# param - The root window
# param - The side panel frame in the root window
def resize(event, root, side_panel):
    # check event is not the initial setup none call
    # Check if the event is from the main window 
    # (otherwise do nothing)
    if event is not None and event.widget is not root:
        return

    # updates labels and radio button's font size based on window size
    width = root.winfo_width()
    for object in gui_objects:
        # scale labels and buttons
        if (isinstance(object,tk.Label) or 
        isinstance(object,tk.Radiobutton) or
        isinstance(object,tk.Listbox) or
        isinstance(object,tk.Button)):
            font_size = max(7, int(width * object._font_scale)-3)
            if getattr(object, "_font_size",None) != font_size:
                object.config(font=("Arial", font_size))
                object._font_size = font_size
        else:
            raise ValueError("Unrecognized tk module at resize")
            
    
    # removes the decorative image if not enough space to fit
    if width < 700:
        side_panel.grid_remove()
    else:
        side_panel.grid()   
       
             
if __name__ == "__main__":
    main()
    