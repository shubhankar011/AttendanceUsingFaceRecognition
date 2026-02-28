import os, json, hashlib, tkinter as tk
from tkinter import filedialog
from PyQt6.QtWidgets import QInputDialog, QLineEdit

BASE_CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".attendance_system")
if not os.path.exists(BASE_CONFIG_PATH):
    os.makedirs(BASE_CONFIG_PATH)

MASTER_CONF = os.path.join(BASE_CONFIG_PATH, "master_path.json")

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
        "class": None,
        "code": None
    }

    with open(MASTER_CONF, "w") as f:
        json.dump({"db_root": directory}, f)

    with open(os.path.join(directory, "dir.json"), "w") as f:
        json.dump(setup_data, f, indent=4)
        
    return setup_data

def saving(data):
    local_config_path = os.path.join(data['directory'], "dir.json")
    with open(local_config_path, "w") as f:
        json.dump(data, f, indent=4)

def hash_pw(pin):
    return hashlib.sha256(str(pin).encode()).hexdigest()

def makingSetup(data, parent):
    name, ok1 = QInputDialog.getText(parent, "Setup", "Enter your Class:")
    if ok1 and name:
        data['class'] = name
        pin, ok2 = QInputDialog.getText(parent, "Setup", "Enter 4-Pin Code:", QLineEdit.EchoMode.Password)
        if ok2 and pin:
            data['code'] = hash_pw(pin)
            saving(data)
            return True
    return False

def save_student_info(data, name, roll_no):
    json_path = data['student_json']
    students = []
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            students = json.load(f)
    students.append({"name": name, "roll_no": roll_no})
    with open(json_path, "w") as f:
        json.dump(students, f, indent=4)