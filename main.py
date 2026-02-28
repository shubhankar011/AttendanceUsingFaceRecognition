import dataHandler
import img_catcher
import recogniser
import os

def main():
    print("System Started...")
    data = dataHandler.loading()
    # print(f"Data is: {data}")
    if data['class'] == None:
        dataHandler.makingSetup(data)
    
    if len(os.listdir(data['path'])) == 0:
        print("No students are registered. Do you want to register first?", end=" ")
        choice = input().lower()
        if choice == 'yes' or choice == 'y':
            img_catcher.faceCreator(data['path'])
    
    while True:
        print("1. Registering \n2. Attending \n3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            checker = int(input("Enter code: "))
            if dataHandler.hash_pw(checker) == data['code']:
                img_catcher.faceCreator(data['path'])
        
        elif choice == 2:
            register = recogniser.recognise(data['path'],img_catcher.capture(data['folder']))
        
        elif choice == 3:
            break
if __name__ == "__main__":
    main()