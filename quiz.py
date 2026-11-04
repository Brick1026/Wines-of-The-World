from math import inf
import tkinter as tk

import numpy as np
import recommender as r
from statistics import mean

class quiz:
    
    def __init__(self,root):
        # the quiz panel
        self.quiz_frame = tk.Frame(
            root,
            borderwidth=1,
            relief="solid",
            highlightthickness=1,
            highlightbackground="#2B2B2B",
            highlightcolor="#2B2B2B",
            bg="#EBE9EC"
        )
        # make objects in quiz grid center
        self.quiz_frame.grid_columnconfigure(0, weight=1)
        self.quiz_frame.grid(row=1, column=0, sticky="nsew",padx=10,pady=10)
        # the next slot on the grid of the root to put a question
        self.next_slot = 0
        
    # param - {array of int} of size n with scalers for each element
    # param - {string} question for the label
    # param - {2d array of strings} for each button name and value [0] = name [1] = value
    # param - {array of objects} the array containing all of the gui objects, 
    #                            just so we can append to it
    # return tk.StringVar to moniter the value
    # Create a multiple choice question with n adjacent multiple choice options
    def make_mult_choice_question(self,scalers,question,options,gui_objects):
        # begin creating gui
        q1_label = tk.Label(self.quiz_frame,text=question,bg="#EBE9EC")
        q1_label.grid(row=self.next_slot, column=0, pady=(10, 5),columnspan=2)
        self.next_slot+=1
        q1_label._font_scale = scalers[0]
        gui_objects.append(q1_label)
        
        # create frame that holds all the buttons
        q1_frame = tk.Frame(self.quiz_frame)
        q1_frame._font_scale = scalers[1]
        q1_frame.grid(row=self.next_slot, column=0, sticky="n",columnspan=2)
        self.next_slot+=1
        var = tk.StringVar(self.quiz_frame,"None")
        
        # for each button defined in options make a button
        for index, option in enumerate(options):
            opt = tk.Radiobutton(q1_frame, 
                                 text=option[0],
                                 variable=var,
                                 value=option[1],
                                 bg="#EBE9EC",
                                 activebackground="#EBE9EC")
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
    def make_mult_select_question(self,scalers,question,options,gui_objects):
        # begin creating gui
        q1_label = tk.Label(self.quiz_frame,text=question,bg="#EBE9EC")
        q1_label.grid(row=self.next_slot, column=0, pady=(10, 5),columnspan=2)
        self.next_slot+=1
        q1_label._font_scale = scalers[0]
        gui_objects.append(q1_label)
        
        # create frame that holds all the buttons
        q1_frame = tk.Frame(self.quiz_frame)
        q1_frame._font_scale = scalers[1]
        q1_frame.grid(row=self.next_slot, column=0, sticky="n",columnspan=2)
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

    # Creates the survey submit button
    # param - int scaler for font size
    # param - text on the button
    # param - the survey answer variables and widgets
    # param - the lsit of gui objects from main
    # param - the function the submit button calls
    # param - the window
    # param - inc_row - boolean if we want to increment the row number
    def make_submit_button(self,scaler,button_text,elems,gui_objects,function,window,inc_row):
        # when we submit answers, unpack them as their integer values and pass to 
        # function to start recommender algorithm
        def submit_answers():
            # unpack my elements
            params = tuple(
                # if this is a listBox then we make a list of floats
                tuple(elem.get(index) for index in elem.curselection())
                if isinstance(elem, tk.Listbox)
                else (
                    # case to handle the submit button for a rating
                    elem
                    if isinstance(elem,dict)
                    # otherwise assign the float value
                    else(
                        # generic cases
                        None
                        if elem.get() in (None,"None")
                        else
                        float(elem.get())
                    )
                )
                for elem in elems
            )
            # launch get_recommender window
            function(window,params)

        # build the submit button bound to the passed function
        submit = tk.Button(self.quiz_frame, text=button_text, 
                           command=submit_answers,
                           bg="#EBE9EC")
        submit.grid(row=self.next_slot, sticky='nsew', column=0, padx=3,pady=3)
        submit._font_scale = scaler
        if inc_row:
            self.next_slot+=1
        gui_objects.append(submit)
    
    
    # make simple button bound to a command 
    # param - int scaler for font size
    # param - text on the button
    # param - a function to bind to the button
    # param - the lsit of gui objects from main
    # param - inc_row - boolean if we want to increment the row number
    # return - the button
    def make_simple_command_button(self,scaler,button_text,gui_objects,function,inc_row):
        button = tk.Button(self.quiz_frame, text=button_text, 
                                   command=function,
                                   bg="#EBE9EC")
        button.grid(row=self.next_slot, sticky='nsew', column=1, padx=3,pady=3)
        button._font_scale = scaler
        self.next_slot+=1
        gui_objects.append(button)
        return button
        
    
        
            
