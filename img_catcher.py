import cv2
import os
import dataHandler

def brighten_face(img_path):
    img = cv2.imread(img_path)
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    res = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    cv2.imwrite(img_path, res)

def Camera(i,path, name = "capture"):
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
        if key == ord('s') or key == ord('S'):
            img_name = f"{name}.jpg"
            full_path = os.path.join(path, img_name)
            cv2.imwrite(full_path, frame)
            print(f"Saved: {full_path}")
            counter += 1
            brighten_face(full_path)
            break
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    if i == 1: 
        return full_path
          
def faceCreator(save_path, name):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    Camera(0,save_path,name)
    
def capture(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return Camera(1,folder)