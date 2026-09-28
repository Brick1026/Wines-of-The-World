# Main GUI runloop

import tkinter as tk
from tkinter import ttk
import quiz as q
from load import load
from PIL import Image, ImageTk

# list of on screen gui objects
gui_objects = []

def main():
    
    load()
    my_quiz = q.quiz()
    
    root = tk.Tk()
    
    # defines the next avaliable grid slot used by question
    root.resizable(height = True, width = True)
    root.title("Wine Curator") 
    root.geometry("710x900")
    root.grid_propagate(False)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    
    
    # the quiz panel
    quiz_frame = tk.Frame(root,borderwidth=5, relief="ridge")
    # make objects in quiz grid center
    quiz_frame.grid_columnconfigure(0, weight=1)
    
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
                anchor="center"
            )
    
    # define the overall page layout
    title.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 5))
    quiz_frame.grid(row=1, column=0, sticky="nsew",padx=10,pady=10)
    side_panel.grid(row=1, column=1, sticky="nsew",padx=10,pady=10)
    
    # have to declare even if not using
    img_label._font_scale = 0 
    img_label.pack(fill="both", expand=True)
    gui_objects.append(img_label)
    
    type_preference = my_quiz.make_question(
                        (.013,.01,.01,.01,.01,.01,.01),                
                        "What is your preferred wine type?",     
                        (["Fortified",1],["Red",2],["White",3],["Sparkling",4],["Dessert",5]), 
                        gui_objects, quiz_frame)                     
    
    acid_preference = my_quiz.make_question(
                        (.013,.01,.01,.01,.01),                
                        "What is your preferred wine acidity?", 
                        (["Low",1],["Medium",2],["High",3]),   
                        gui_objects, quiz_frame)         
                                                
    abv_preference = my_quiz.make_question(
                        (.013,.01,.01,.01,.01),                
                        "What is your preferred abv?", 
                        (["Low (8-12.5%)",1],["Medium (12.5-13.5%)",2],["High (13.5%+)",3]),   
                        gui_objects, quiz_frame)    
        
    body_preference = my_quiz.make_question(
                        (.013,.01,.01,.01,.01),                
                        "What is your preferred wine body?", 
                        (["Light",1],["Medium",2],["Full",3]),   
                        gui_objects, quiz_frame)    
    
    
    world_preference = my_quiz.make_question(
                        (.013,.01,.01,.01),                
                        "Do you prefer old world or new world wine?", 
                        (["Old World",1],["New World",2]),   
                        gui_objects, quiz_frame)    
    
    # add grape preference question

    # configure the lambda event to call resize on configure
    root.bind("<Configure>", lambda event: resize(event, root, side_panel))
    root.after_idle(lambda: resize(None, root, side_panel))
    root.mainloop()
    

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
        if isinstance(object,tk.Label) or isinstance(object,tk.Radiobutton):
            font_size = max(7, int(width * object._font_scale))
            if getattr(object, "_font_size",None) != font_size:
                object.config(font=("Arial", font_size))
                object._font_size = font_size
    
    # removes the decorative image if not enough space to fit
    if width < 700:
        side_panel.grid_remove()
    else:
        side_panel.grid()   
       
                   
if __name__ == "__main__":
    main()