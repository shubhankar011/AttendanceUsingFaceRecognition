import os
import warnings, logging,json

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings('ignore')
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Above code is there to remove the warnings and loggings made by Tensorflow and DeepFace. Don't remove it

from deepface import DeepFace
import pandas as pd
import csv, datetime

def logging_attendance(img_path):
    name = os.path.basename(img_path)
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    with open("attendance_log.csv", mode='r',newline='') as f:
        if f"{name},{today}" in f.read():
                print(f"{name} is already marked present for today.")
                return

    with open("attendance_log.csv", mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            name, 
            datetime.datetime.now().strftime('%Y-%m-%d'), 
            datetime.datetime.now().strftime('%H:%M:%S')
        ])

    print(f"Attendance recorded in CSV for {name}")

def analyzing(db_path):
    print("Scanning database to update memory...")
    all_files = [f for f in os.listdir(db_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
    
    if not all_files:
        print("Database folder is empty. Nothing to analyze.")
        return

    DeepFace.find(img_path = os.path.join(db_path, all_files[0]), 
                  db_path = db_path, 
                  model_name = 'VGG-Face', 
                  enforce_detection = False,
                  distance_metric='cosine'
                  )
    
    print("Analysis complete. Memory file (.pkl) created.")

def recognise(db_path, img_path):
    results = DeepFace.find(img_path, 
                            db_path = db_path, 
                            model_name = 'VGG-Face', 
                            enforce_detection = False,
                            distance_metric='cosine'
                            )
    
    if len(results) > 0 and not results[0].empty:
        row = results[0].iloc[0]
        distance = row['distance']

        if distance < 0.55: 
            matched_name = os.path.basename(row['identity']).split('.')[0]
            
            roll_no = None
            if os.path.exists("student.json"):
                with open("student.json", "r") as f:
                    students = json.load(f)
                    for s in students:
                        if s['name'] == matched_name:
                            roll_no = s['roll_no']
                            break

            print(f"Match found! Name: {matched_name} | Roll: {roll_no}")
            logging_attendance(row['identity']) 
            return matched_name
        else:
            print(f"Person looks familiar (Dist: {distance:.2f}), but not sure enough.")

    else:
        print("No match found.")

    return results

