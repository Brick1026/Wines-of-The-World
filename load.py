# File which handles the loading screen before handing back off to main loop

import tkinter as tk
import threading
from fetch import fetch as f

_loading = None
_fetch = None

class load():
    def __init__(self):
        self._loading = tk.Tk()
        # spawn secondary thread to spawn query threads
        self._fetch = threading.Thread(target=f,daemon=True)
        self._loading.title("Parsing Grapes") 
        self._loading.mainloop()
    
    def destroy():
        _loading.destroy()