import tkinter as tk
from tkinter import filedialog
import json 
import os

root = tk.Tk()
root.withdraw()
DB_FILE = "dir.json"

def loading():
    if not os.path.exists(DB_FILE):
        path = "dp_path"
        folder = "folder"
        directory = filedialog.askdirectory(title="Select a Folder")
        path = directory + path
        folder = directory + folder
        return {"folder":folder,"path":path,"directory":directory}
    
    with open(DB_FILE, "r") as f:
        return json.load(f)

def saving(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)