import os
import warnings, logging

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings('ignore')
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Above code is there to remove the warnings and loggings made by Tensorflow and DeepFace. Don't remove it
from deepface import DeepFace
import pandas as pd

db_path = "D:/FaceRecognitionDatabase/db_path"

def recognise():
    results = DeepFace.find(img_path = "img1.jpg", 
                            db_path = db_path, 
                            model_name = 'VGG-Face', 
                            enforce_detection = False)

    # 'results' is a list of Pandas DataFrames
    if len(results) > 0 and not results[0].empty:
        # Get the top match
        best_match = results[0].iloc[0]['identity']
        print(f"Match found! This looks like: {best_match}")
    else:
        print("No match found in the database.")
recognise()

