import dataHandler
import img_catcher
import recogniser
import os

def student_info(data):
    registered_new = False
    print("\nStudent Registration")
    while True:
        name = input("Enter Student Name (or 'q' to quit): ").strip().replace(" ","_")
        if name.lower() == 'q': 
            break
        roll_no = input("Enter Roll Number: ").strip()
        dataHandler.save_student_info(data, name, roll_no)
        img_catcher.faceCreator(data['path'], name=name)
                    
        registered_new = True
        print(f"Captured images for {name}.")

    if registered_new:
                    print("Updating AI memory for all new registrations...")
                    dataHandler.refresh_db(data['path'])

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
            student_info(data)
    
    while True:
        print("1. Registering \n2. Attending \n3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            checker = input("Enter code: ") 
            if dataHandler.hash_pw(checker) == data['code']:
                student_info(data)
        
        elif choice == 2:
            register = recogniser.recognise(data['path'],img_catcher.capture(data['folder']), data['directory'], data['student_json'])
        
        elif choice == 3:
            break
if __name__ == "__main__":
    main()