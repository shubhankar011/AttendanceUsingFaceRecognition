import os
import warnings, logging

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings('ignore')
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Above code is there to remove the warnings and loggings made by Tensorflow and DeepFace. Don't remove it
from deepface import DeepFace
import pandas as pd

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
            print(f"Match found! {row['identity']} (Dist: {distance:.2f})")
            return row['identity']
        else:
            print(f"Person looks familiar (Dist: {distance:.2f}), but not sure enough.")

    else:
        print("No match found.")

    return results

