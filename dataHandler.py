import tkinter as tk
from tkinter import filedialog
import json, os, hashlib

root = tk.Tk()
root.withdraw()
DB_FILE = "dir.json"
entry = tk.Entry(root)

def loading():
    if not os.path.exists(DB_FILE):
        path = "dp_path"
        folder = "folder"
        directory = filedialog.askdirectory(title="Select a Folder")
        path = directory + path
        folder = directory + folder
        os.makedirs(folder)
        os.makedirs(path)
        return {"folder":folder,"path":path,"directory":directory,"class":None}
    
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