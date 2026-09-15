# Main GUI runloop

import tkinter as tk
from load import load

def main():
    load()
    root = tk.Tk()
    root.resizable(height = True, width = True)
    root.title("Wine Curator") 
    root.mainloop()
        
if __name__ == "__main__":
    main()