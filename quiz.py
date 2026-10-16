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
    def make_mult_choice_question(self,scalers,question,options,gui_objects,root):
        # begin creating gui
        q1_label = tk.Label(root,text=question,bg="#EBE9EC")
        q1_label.grid(row=self.next_slot, column=0, pady=(10, 5))
        self.next_slot+=1
        q1_label._font_scale = scalers[0]
        gui_objects.append(q1_label)
        
        # create frame that holds all the buttons
        q1_frame = tk.Frame(root)
        q1_frame._font_scale = scalers[1]
        q1_frame.grid(row=self.next_slot, column=0, sticky="n" )
        self.next_slot+=1
        var = tk.StringVar(root,"None")
        
        # for each button defined in options make a button
        for index, option in enumerate(options):
            opt = tk.Radiobutton(q1_frame, 
                                 text=option[0],
                                 variable=var,
                                 value=option[1],
                                 bg="#EBE9EC")
            opt._font_scale = scalers[index+2]
            opt.grid(row=self.next_slot,column=index,sticky='w')
            gui_objects.append(opt)
            
        self.next_slot+=1
        return var
    
    # param - {array of int} of size n with scalers for each element
    # param - {string} question for the label
    # param - {2d array of strings} for each button name and value [0] = name [1] = value
    # param - {array of objects} the array containing all of the gui objects, 
    #                            just so we can append to it
    # param - {root} the root to build the quiz on
    # return tk.Listbox containing the multiple-select options
    def make_mult_select_question(self,scalers,question,options,gui_objects,root):
        # begin creating gui
        q1_label = tk.Label(root,text=question,bg="#EBE9EC")
        q1_label.grid(row=self.next_slot, column=0, pady=(10, 5))
        self.next_slot+=1
        q1_label._font_scale = scalers[0]
        gui_objects.append(q1_label)
        
        # create frame that holds all the buttons
        q1_frame = tk.Frame(root)
        q1_frame._font_scale = scalers[1]
        q1_frame.grid(row=self.next_slot, column=0, sticky="n" )
        self.next_slot+=1
        listbox = tk.Listbox(
            q1_frame,
            selectmode=tk.MULTIPLE,
            height=max(1, min(len(options), 8)),
            width=26,
            background="white",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#B8B4B9",
            selectbackground="#6B2737",
            selectforeground="white",
            activestyle="none",
            exportselection=False,
        )
        listbox._font_scale = scalers[2]  # one scale applies to every item
        listbox.grid(row=self.next_slot, column=0, sticky="nsew")
        scrollbar = tk.Scrollbar(q1_frame, orient=tk.VERTICAL, command=listbox.yview)
        scrollbar.grid(row=self.next_slot, column=1, sticky="ns")
        listbox.configure(yscrollcommand=scrollbar.set)

        for grape, _ in options:
            listbox.insert(tk.END, grape.title())
            
        gui_objects.append(listbox) 
        self.next_slot+=1
        return listbox
