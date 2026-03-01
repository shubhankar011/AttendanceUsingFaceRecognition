import tkinter as tk
from tkinter import filedialog
import json, os, hashlib, csv
import recogniser

BASE_CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".attendance_system")
if not os.path.exists(BASE_CONFIG_PATH):
    os.makedirs(BASE_CONFIG_PATH)

MASTER_CONF = os.path.join(BASE_CONFIG_PATH, "master_path.json")

def save_student_info(data, name, roll_no):
    STUDENT_DB = data['student_json']
    students = []
    if os.path.exists(STUDENT_DB):
        with open(STUDENT_DB, "r") as f:
            students = json.load(f)
    with open(STUDENT_DB, 'r') as f:
        st = json.load(f)
        for i in st:
            if roll_no in st:
                print("It is already registered!!!")
                return
    students.append({
        "name": name, 
        "roll_no": roll_no
    })
    
    with open(STUDENT_DB, "w") as f:
        json.dump(students, f, indent=4)
    print(f"Successfully registered {name} (Roll: {roll_no})")

def loading():
    if os.path.exists(MASTER_CONF):
        with open(MASTER_CONF, "r") as f:
            m_data = json.load(f)
            root_dir = m_data.get("db_root")
        
        dir_file = os.path.join(root_dir, "dir.json")
        if os.path.exists(dir_file):
            with open(dir_file, "r") as f:
                return json.load(f)

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    directory = filedialog.askdirectory(title="Select your Attendance Database Folder")
    root.destroy()
    
    if not directory: return None

    path = os.path.join(directory, "dp_path") 
    folder = os.path.join(directory, "folder") 
    if not os.path.exists(path): os.makedirs(path)
    if not os.path.exists(folder): os.makedirs(folder)

    setup_data = {
        "directory": directory,
        "path": path,
        "folder": folder,
        "student_json": os.path.join(directory, "student.json"),
        "att_dir": os.path.join(directory,"attendance_log.csv"),
        "class": None,
        "code": None
    }

    with open(MASTER_CONF, "w") as f:
        json.dump({"db_root": directory}, f)

    with open(os.path.join(directory, "dir.json"), "w") as f:
        json.dump(setup_data, f, indent=4)
        
    return setup_data
    return setup_data

def saving(data):
    DB_FILE = os.path.join(data['directory'], "dir.json")
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

def showData(st_db):
    with open(st_db, 'r') as f:
            data = json.load(f)
            print("Total Students are: ", len(data))
            print("-"*10)
            alt = True
            for i in data:
                for key,value in i.items():
                    print(key,value)
                print("-"*10)
