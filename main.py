# Main GUI runloop

import tkinter as tk

from load import load

# list of on screen gui objects
gui_objects = []
# scaler for gui objects relative to window
scalers = [[.02,.1],[.5,.1],[.5,.1],[.5,.1],[.5,.1]]

def main():
    
    load()
    root = tk.Tk()
    root.resizable(height = True, width = True)
    root.title("Wine Curator") 
    root.bind("<Configure>", lambda event: resize(event.widget))
    
    # begin creating gui
    q1 = tk.Label(root,text="What is your prefered wine acidity")
    q1.place(relx=0.5, rely=0.05, anchor="n", relwidth=0.9)
    gui_objects.append(q1)
    
    
    # first resize before main loop
    resize(root)
    root.mainloop()
    

# Resizes all widgets in GUI
# param - takes the root window
def resize(root):
    width = root.winfo_width()
    height = root.winfo_height()
    for index, object in enumerate(gui_objects):
        if isinstance(object,tk.Label):
            font_size = max(8, int(width * scalers[index][0]))
            if getattr(object, "_font_size",None) != font_size:
                object.config(font=("Arial", font_size))
                object._font_size = font_size
                
                
if __name__ == "__main__":
    main()