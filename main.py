# Main GUI runloop

import tkinter as tk
import quiz as q
from load import load

# list of on screen gui objects
gui_objects = []

# fixed constant to make sure grid can fit all questions
_QUIZ_SIZE = 10

def main():
    
    load()
    my_quiz = q.quiz()
    
    root = tk.Tk()
    # defines the next avaliable grid slot used by question
    root.resizable(height = True, width = True)
    root.title("Wine Curator") 
    root.grid_propagate(False)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(_QUIZ_SIZE, weight=1)
    
    type_preference = my_quiz.make_question(
                        (.013,.01,.01,.01,.01,.01,.01),                
                        "What is your preferred wine type",     
                        (["Fortified",1],["Red",2],["White",3],["Sparkling",4],["Dessert",5]), 
                        gui_objects, root)                     
    
    acid_preference = my_quiz.make_question(
                        (.013,.01,.01,.01,.01),                
                        "What is your preferred wine acidity", 
                        (["low",1],["medium",2],["high",3]),   
                        gui_objects, root)                                                     
    
    body_preference = my_quiz.make_question(
                        (.013,.01,.01,.01,.01),                
                        "What is your preferred wine body", 
                        (["light",1],["medium",2],["Full",3]),   
                        gui_objects, root)    
    
    abv_preference = my_quiz.make_question(
                        (.013,.01,.01,.01,.01),                
                        "What is your preferred abv", 
                        (["low (8-12.5%)",1],["medium (12.5-13.5%)",2],["high (13.5%+)",3]),   
                        gui_objects, root)    


    
    root.bind("<Configure>", lambda event: resize(event, root))
    root.after_idle(lambda: resize(None, root))
    root.mainloop()
    

# Resizes all widgets in GUI
# param - takes the root window
def resize(event, root):
    # check event is not the initial setup none call
    # Check if the event is from the main window 
    # (otherwise do nothing)
    if event is not None and event.widget is not root:
        return

    width = root.winfo_width()
    for object in gui_objects:
        if isinstance(object,tk.Label) or isinstance(object,tk.Radiobutton):
            font_size = max(10, int(width * object._font_scale))
            if getattr(object, "_font_size",None) != font_size:
                object.config(font=("Arial", font_size))
                object._font_size = font_size
                   
if __name__ == "__main__":
    main()