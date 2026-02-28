import tkinter as tk
from tkinter import filedialog
import json, os, hashlib
import recogniser

DB_FILE = "dir.json"
STUDENT_DB = "student.json"

def save_student_info(name, roll_no):
    students = []
    if os.path.exists(STUDENT_DB):
        with open(STUDENT_DB, "r") as f:
            students = json.load(f)
    
    students.append({
        "name": name, 
        "roll_no": roll_no
    })
    
    with open(STUDENT_DB, "w") as f:
        json.dump(students, f, indent=4)
    print(f"Successfully registered {name} (Roll: {roll_no})")

def loading():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            data = json.load(f)
        
        if os.path.exists(data.get('path', '')) and os.path.exists(data.get('folder', '')):
            root.destroy()
            return data

    print("System not initialized or folders missing. Opening folder selection...")
    directory = filedialog.askdirectory(title="Select a Folder to save your Database")
    root.destroy()

    if not directory:
        print("No directory selected. Exiting...")
        exit()

    path = os.path.join(directory, "dp_path")
    folder = os.path.join(directory, "folder")
    
    if not os.path.exists(path): os.makedirs(path)
    if not os.path.exists(folder): os.makedirs(folder)
    
    setup_data = {"folder": folder, "path": path, "directory": directory, "class": None}
    
    saving(setup_data)
    
    return setup_data

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