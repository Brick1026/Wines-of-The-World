import tkinter as tk

class quiz:
    next_slot = 0
    
    def __init__(self):
        # the next slot on the grid of the root to put a question
        self.next_slot = 0
        
    # param - {array of int} of size n with scalers for each element
    # param - {string} question for the label
    # param - {2d array of strings} for each button name and value [0] = name [1] = value
    # param - {array of objects} the array containing all of the gui objects, 
    #                            just so we can append to it
    # param - {root} the root to build the quiz on
    # return tk.StringVar to moniter the value
    # Create a multiple choice question with n adjacent multiple choice options
    def make_question(self,scalers,question,options,gui_objects,root):
        # begin creating gui
        q1_label = tk.Label(root,text=question)
        q1_label.grid(row=self.next_slot, column=0, pady=(10, 5))
        self.next_slot+=1
        q1_label._font_scale = scalers[0]
        gui_objects.append(q1_label)
        
        # create frame that holds all the buttons
        q1_frame = tk.Frame(root)
        q1_frame._font_scale = scalers[1]
        q1_frame.grid(row=self.next_slot, column=0, sticky="n")
        self.next_slot+=1
        var = tk.StringVar(root,"None")
        
        # for each button defined in options make a button
        for index, option in enumerate(options):
            opt = tk.Radiobutton(q1_frame, text=option[0],variable=var,value=option[1])
            opt._font_scale = scalers[index+2]
            opt.grid(row=self.next_slot,column=index,sticky='ew')
            gui_objects.append(opt)
            
        self.next_slot+=1
        return var
    
