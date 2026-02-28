import os, warnings, logging, json, csv, datetime

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings('ignore')
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Above code is there to remove the warnings and loggings made by Tensorflow and DeepFace. Don't remove it

from deepface import DeepFace

def logging_attendance(img_path, base_dir):
    name = os.path.basename(img_path).split('.')[0]
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    att_file = os.path.join(base_dir, "attendance_log.csv")

    if not os.path.exists(att_file):
        with open(att_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Date", "Time"])

    with open(att_file, mode='r', newline='') as f:
        if f"{name},{today}" in f.read():
            return f"{name} already marked."

    with open(att_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, today, datetime.datetime.now().strftime('%H:%M:%S')])
    return f"Attendance recorded for {name}"

def analyzing(db_path):
    all_files = [f for f in os.listdir(db_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
    if not all_files: return
    DeepFace.find(
                    img_path=os.path.join(db_path, all_files[0]), 
                    db_path=db_path, 
                    model_name='VGG-Face', 
                    enforce_detection=False
                )

def recognise(db_path, img_path, student_path):
    try:
        results = DeepFace.find(
            img_path, 
            db_path = db_path, 
            model_name = 'VGG-Face', 
            enforce_detection = False,
            distance_metric='cosine'
        )
    except Exception as e:
        print(f"DeepFace Error: {e}")
        return None, None
    
    if len(results) > 0 and not results[0].empty:
        row = results[0].iloc[0]
        if row['distance'] < 0.55: 
            matched_name = os.path.basename(row['identity']).split('.')[0]
            roll_no = "Unknown"
            
            if os.path.exists(student_path):
                with open(student_path, "r") as f:
                    students = json.load(f)
                    for s in students:
                        if s['name'] == matched_name:
                            roll_no = s.get('roll_no')
                            break

            log_msg = logging_attendance(row['identity'], os.path.dirname(student_path))
            return matched_name, roll_no, log_msg
    return None, None