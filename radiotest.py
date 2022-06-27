
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
import radiotest.config.config as config
import radiotest.drivers.loader as loader
import radiotest.gui.classes as gui

""""
config.Loader_obj = loader.Loader()

config.Loader_obj.add_instrument("ARB1", "Arbitrary Waveform Generator", "sdg1032x", "Sdg1032x", interface="vxi", hostname="SDG-1032X")
config.Loader_obj.add_instrument("SA1", "Spectrum Analyzer", "dsa815", "Dsa815", interface="vxi", hostname="DSA-815")

sa_info = config.Loader_obj.load("SA1")
sa = config.Loader_obj.get_driver_instance(sa_info)

arb_info = config.Loader_obj.load("ARB1")
arb = config.Loader_obj.get_driver_instance(arb_info)
"""

# GUI initialization

Root = tk.Tk()
Root.title("RadioTest")
config.App_obj = gui.FullScreenApp(Root)
config.App_obj.pack(side="top", fill="both", expand=True)

#notebook = ttk.Notebook(Root)
#notebook.pack(pady=10, expand=True)

#frame1 = ttk.Frame(notebook, width=400, height = 280)
#frame2 = ttk.Frame(notebook, width=400, height = 280)

#frame1.pack(fill='both', expand=True)
#frame2.pack(fill='both', expand=True)

#notebook.add(frame1, text='General Information')
#notebook.add(frame2, text='Profile')


Root.mainloop()
