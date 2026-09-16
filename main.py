# Main GUI runloop

import tkinter as tk

from load import load

# param - array of n scalers for each element
# 
# Create a multiple choice question with a 
def make_question():
    return
    

# list of on screen gui objects
gui_objects = []
# scaler for gui objects relative to window
scalers = [.013,.01,.01,.01,.01,.01,.01,.01]

def main():
    
    load()
    root = tk.Tk()
    root.resizable(height = True, width = True)
    root.title("Wine Curator") 
    root.grid_propagate(False)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    
    # begin creating gui
    q1_label = tk.Label(root,text="What is your prefered wine acidity")
    q1_label.grid(row=0, column=0, pady=(10, 5))
    q1_label._font_scale = scalers[0]
    gui_objects.append(q1_label)
    
    q1_frame = tk.Frame(root)
    q1_frame._font_scale = scalers[1]
    q1_frame.grid(row=1, column=0, sticky="n")
    acid_preference = tk.StringVar(root,"None")
    
    q1_ans1 = tk.Radiobutton(q1_frame, text="low",variable=acid_preference,value="low")
    q1_ans1._font_scale = scalers[2]
    q1_ans1.grid(row=0,column=0)
    gui_objects.append(q1_ans1)
    
    q1_ans2 = tk.Radiobutton(q1_frame, text="medium",variable=acid_preference,value="medium")
    q1_ans2._font_scale = scalers[3]
    q1_ans2.grid(row=0,column=1)
    gui_objects.append(q1_ans2)
    
    q1_ans3 = tk.Radiobutton(q1_frame, text="high",variable=acid_preference,value="high")
    q1_ans3._font_scale = scalers[4]
    q1_ans3.grid(row=0,column=2)
    gui_objects.append(q1_ans3)
    
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