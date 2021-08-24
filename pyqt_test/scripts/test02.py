import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
import rospy 
from std_msgs.msg import String
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QInputDialog, QVBoxLayout, QMessageBox

form_class = uic.loadUiType("main2.ui")[0]

class WindowClass(QMainWindow, form_class) :

    running = False
    isbtn12 = False

    def __init__(self) :
        super(WindowClass,self).__init__()
        self.setupUi(self)
        self.LibrarianBtn.clicked.connect(self.librarianMode)
        self.StudentBtn.clicked.connect(self.StudentMode)
        

    def librarianMode(self):
        print("hello library")
        #whatever it is .. 
        #barcode 

    def cv2Show(self):
        global running, secondStep
        running = True
        secondStep = False
        cap = cv2.VideoCapture(0)

        while(running):
            ret, frame = cap.read()
            #pub = rospy.Publisher('chatter',String,queue_size = 10)
            #rospy.init_node('talker',anonymous = True)

            if not ret:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            decoded = pyzbar.decode(gray)
            
            for d in decoded:
                x,y,w,h = d.rect
                barcode_data = d.data.decode("utf-8")
                #print(type(barcode_data))
                #unicode
                barcode_type = d.type
                cv2.rectangle(frame,(x,y),(x+w,y+h), (0,0,255),2)
                text='%s(%s)'%(barcode_data, barcode_type)
                cv2.putText(frame,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2,cv2.LINE_AA)
                send_str = barcode_data
                #print(type(send_str))
                #unicode
                #rospy.loginfo(send_str)
                #pub.publish(send_str)
                #rospy.sleep(0.25)

                if(barcode_data.find("2") != -1):
                    print("accepted")
                    running = False
                    QMessageBox.about(self, "Accept message", "You are accepted")
                    self.BookEnter()
                else:
                   QMessageBox.about(self, "Decline message", "You are denied") 
                    
            cv2.imshow('frame',frame)       


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        running = False
        

    def StudentMode(self):
        print("hello student")
        self.cv2Show()



    def BookEnter(self):

        global isbtn12
        isbtn12 = True
        print("to the next level")
        btn3 = QPushButton('Book Title', self)
        btn3.move(500, 500)
        btn3.clicked.connect(self.showDialog)
        btn3.clicked.connect(btn3.deleteLater)

        btn3.le = QLineEdit(self)
        btn3.le.move(120, 35)

        btn3.setWindowTitle('Input dialog')
        #btn3.setGeometry(300, 300, 300, 200)
        btn3.show()
    
    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter the title of the book:')
        print("rrrr")
        if ok:
            #self.le.setText(str(text))
            print("kkkk")
            QMessageBox.about(self, "Finding path", "Robot is finding path")

            # here goes the line of server 
            if ok:
                #if the robot finished finding the path, 
                QMessageBox.about(self, "Finding path", "Here is the destination")
                print("barcode nawara")
                btn4 = QPushButton('Check out : Barcode Detect', self)
                btn4.move(300, 300)
                btn4.resize(200,200)
                print("barcode nawara22")
                btn4.setStyleSheet("QPushButton"
                                     "{"
                                     "background-color : rgb(255, 190, 11);"
                                     "}"
                                     "QPushButton::pressed"
                                     "{"
                                     "background-color : rgb(251, 86, 7);"
                                     "}")
                btn4.clicked.connect(self.showBarcode)
                btn4.clicked.connect(btn4.deleteLater)

                btn4.show()


    def showBarcode(self):

        print('barcode again')
        self.cv2Show()

    def lastFunc(self):
        pass
        

if __name__ == "__main__" :
    app = QApplication(sys.argv) 

    myWindow = WindowClass() 

    myWindow.show()

    app.exec_()