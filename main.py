# Main GUI runloop

import tkinter as tk
from tkinter import Listbox, ttk
from fetch import get_grapes
import quiz as q
import recommender as r
from load import load
from PIL import Image, ImageTk


# list of on screen gui objects
gui_objects = []

recommender = r.recommender()

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
                               get_recommend_window)
    
    # configure the lambda event to call resize on configure
    root.bind("<Configure>", lambda event: resize(event, root, side_panel))
    root.after_idle(lambda: resize(None, root, side_panel))
    root.mainloop()

# Creates a top level recommendation window
# param - root window
# param - survey answers
def get_recommend_window(root,answers):
    user_sample = recommender.build_user_sample(answers)
    samples = recommender.build_sample_matrix(answers)

    rec_window = tk.Toplevel(root)
    rec_window.title("Recommendation")
    rec_window.geometry("250x250")
    

# Resizes all widgets in GUI
# param - The triggering event
# param - The root winow
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
    