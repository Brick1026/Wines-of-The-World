# Main GUI runloop

import tkinter as tk
import quiz as q
from load import load

# list of on screen gui objects
gui_objects = []

def main():
    
    load()
    my_quiz = q.quiz()
    
    root = tk.Tk()
    # defines the next avaliable grid slot used by question
    root.resizable(height = True, width = True)
    root.title("Wine Curator") 
    root.grid_propagate(False)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    
    acid_preference = my_quiz.make_question(
                          (.013,.01,.01,.01,.01),                # scalers for objects in question
                          "What is your prefered wine acidity",  # question
                          (["low",1],["medium",2],["high",3]),   # options
                          gui_objects, root)                     # obligatory pass throughs                                 
    
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