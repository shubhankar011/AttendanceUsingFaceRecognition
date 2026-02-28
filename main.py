import dataHandler
import img_catcher
import recogniser

def main():
    data = dataHandler.loading()
    if data['class'] == None:
        dataHandler.makingSetup(data)
    
    while True:
        print("1. Registering \n2. Attending \n3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            checker = int(input("Enter code: "))
            if checker == data['code']:
                img_catcher.faceCreator(data['path'])
        
        elif choice == 2:
            register = recogniser.recognise(data['path'],img_catcher.capture(data['folder']))
        
        elif choice == 3:
            break
if __name__ == "__main__":
    main()