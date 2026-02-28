import cv2
import os

def Camera(i,path):
    cap = cv2.VideoCapture(0)
    print("Press 's' to save and 'q' for quit")
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    counter = len(os.listdir(path)) if i == 0 else 0
    full_path = None
    while True:
        ret,frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        cv2.imshow('Live Feed', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            img_name = f"capture_{counter}.jpg"
            full_path = os.path.join(path, img_name)
            cv2.imwrite(full_path, frame)
            print(f"Saved: {full_path}")
            counter += 1
            if i == 1:
                break
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    if i == 1: 
        return full_path
          
def faceCreator(save_path):
    i = 0
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    Camera(i,save_path)
    
def capture(folder):
    i = 1
    if not os.path.exists(folder):
        os.makedirs(folder)
    return Camera(i,folder)