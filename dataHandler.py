import tkinter as tk
from tkinter import filedialog
import json, os, hashlib
import recogniser

DB_FILE = "dir.json"

def loading():
    root = tk.Tk()
    root.withdraw()
    
    if not os.path.exists(DB_FILE):
        path = "dp_path"
        folder = "folder"
        directory = filedialog.askdirectory(title="Select a Folder")
        root.destroy()
        path = os.path.join(directory,path)
        folder = os.path.join(directory,folder)
        os.makedirs(folder)
        os.makedirs(path)
        return {"folder":folder,"path":path,"directory":directory,"class":None}
    
    root.destroy()
    with open(DB_FILE, "r") as f:
        return json.load(f)

def saving(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)
# print(loading())

def hash_pw(pin):
    return hashlib.sha256(str(pin).encode()).hexdigest()

def makingSetup(data):
    data['class'] = input("Enter your class: ")
    pin = int(input("Enter 4-Pin Code: "))
    data['code'] = hash_pw(pin)
    saving(data)

def refresh_db(db_path):
    for file in os.listdir(db_path):
        if file.endswith(".pkl"):
            file_path = os.path.join(db_path, file)
            os.remove(file_path)
            print(f"{file} removed")
    recogniser.analyzing(db_path)