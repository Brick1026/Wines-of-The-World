# File which handles the loading screen before handing back off to main loop

import tkinter as tk
from tkinter import ttk
import threading
from fetch import fetch as f

class load():
    _loading = None
    # Initialize loading window and pawn thread to query
    def __init__(self):
        self._loading = tk.Tk()
        self._loading.title("Parsing Grapes")
        self._loading.geometry('300x200')
        label = tk.Label(self._loading, text="Parsing Grapes, please do not close this window.\n")
        label.pack(ipadx=10, ipady=10)
        self._progress = ttk.Progressbar(self._loading, orient='horizontal', mode='indeterminate', length=250)
        self._progress.pack(pady=20)
        self._progress.start()

        # spawn secondary thread to spawn query threads
        thread = threading.Thread(target=self._run_fetch, daemon=True)
        thread.start()
        
        self._loading.mainloop()

    # Fetch and then stop the loading screen when we are done
    def _run_fetch(self):
        try:
            f()
        finally:
            self._loading.after(0, self.destroy)

    # Called from fetch, destroys loading screen 
    def destroy(self):
        self._progress.stop()
        self._loading.destroy()