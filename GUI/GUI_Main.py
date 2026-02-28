import sys, cv2, os, shutil
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QLabel, QWidget, QTextEdit, QInputDialog, QLineEdit, QMessageBox)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap
import dataHandler
import recogniser

class AttendanceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Attendance System - Pro")
        self.setFixedSize(850, 700)
        
        self.data = dataHandler.loading()

        if self.data is None:
            QMessageBox.warning(self, "Error", "No database folder selected. Please start the application again and select a folder.")
            sys.exit()

        self.camera_label = QLabel("Webcam Feed")
        self.camera_label.setFixedSize(640, 480)
        self.camera_label.setStyleSheet("background-color: black; border: 3px solid #444;")
        
        self.btn_reg = QPushButton("1. Register Student")
        self.btn_attend = QPushButton("2. Mark Attendance")
        self.btn_reset = QPushButton("Reset System")
        self.btn_reset.setStyleSheet("background-color: #f44336; color: white;")
        
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_reg)
        btn_layout.addWidget(self.btn_attend)
        btn_layout.addWidget(self.btn_reset)
        
        layout.addWidget(self.camera_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(btn_layout)
        layout.addWidget(self.log_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.btn_attend.clicked.connect(self.do_attendance)
        self.btn_reg.clicked.connect(self.do_registration)
        self.btn_reset.clicked.connect(self.reset_database)

        if not self.data.get('code') or not self.data.get('class'):
            if not dataHandler.makingSetup(self.data, self):
                sys.exit()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            qt_img = QImage(rgb_frame.data, w, h, ch * w, QImage.Format.Format_RGB888)
            self.camera_label.setPixmap(QPixmap.fromImage(qt_img).scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio))

    def do_attendance(self):
        self.log_box.append("Capturing...")
        ret, frame = self.cap.read()
        if ret:
            temp_img = os.path.join(self.data['folder'], "gui_temp.jpg")
            cv2.imwrite(temp_img, frame)
            
            # db_path = self.data['path'] (the image folder)
            # img_path = temp_img (the current camera frame)
            # student_path = self.data['student_json'] (the student record file)
            image_files = [f for f in os.listdir(self.data['path']) 
                           if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            if not image_files:
                self.log_box.append("Error: No student images found in database.")
                self.log_box.append("Please register a student first.")
                return 
            
            name, roll,log_msg = recogniser.recognise(
                self.data['path'], 
                temp_img, 
                self.data['student_json']
            )
            
            if name:
                self.log_box.append(f"Recognized: {name} (Roll: {roll})")
                self.log_box.append(f"{log_msg}")
            else:
                self.log_box.append("Unknown Person.")

    def do_registration(self):
       
        pin, ok = QInputDialog.getText(self, "Security", "Enter Admin PIN:", QLineEdit.EchoMode.Password)
        if not ok:
            return
        if dataHandler.hash_pw(pin) != self.data['code']:
            self.log_box.append("Access Denied.")
            return

        name, ok_n = QInputDialog.getText(self, "Registration", "Enter Student Name:")
        if not ok_n:
            return

        roll, ok_r = QInputDialog.getText(self, "Registration", "Enter Roll No:")
        if not ok_r:
            return

        if name and roll:
            confirm = QMessageBox.question(self, "Ready?", f"Position {name} in front of camera and click Yes to capture.",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if confirm == QMessageBox.StandardButton.Yes:
                ret, frame = self.cap.read()
                if ret:
                    img_path = os.path.join(self.data['path'], f"{name}.jpg")
                    cv2.imwrite(img_path, frame)
                    dataHandler.save_student_info(self.data, name, roll)
                    self.log_box.append(f"{name} registered successfully!")
                    recogniser.analyzing(self.data['path'])

    def reset_database(self):
        pin, ok = QInputDialog.getText(self, "Danger Zone", "Enter Admin PIN to RESET EVERYTHING:", QLineEdit.EchoMode.Password)
        if not ok:
            return
        if dataHandler.hash_pw(pin) != self.data['code']:
            self.log_box.append("Access Denied.")
            return

        confirm = QMessageBox.warning(self, "Confirm Reset", "This will delete ALL students and images. Proceed?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes:

            if os.path.exists(self.data['path']): shutil.rmtree(self.data['path'])
            if os.path.exists(self.data['student_json']): os.remove(self.data['student_json'])

            os.makedirs(self.data['path'], exist_ok=True)
            os.makedirs(self.data['folder'], exist_ok=True)

            self.data['code'] = None
            self.data['class'] = None
            dataHandler.saving(self.data)

            self.log_box.append("Database cleared. Please restart the application.")
            QMessageBox.information(self, "Success", "Database cleared. Please restart the application.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttendanceApp()
    window.show()
    sys.exit(app.exec())