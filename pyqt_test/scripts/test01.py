#!/usr/bin/env python

import sys
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
import rospy 
from std_msgs.msg import String
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QInputDialog, QVBoxLayout, QMessageBox


form_class = uic.loadUiType("main2.ui")[0]



class MyApp(QWidget, form_class):

    running = False
    isbtn12 = False

    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()
        self.setupUi(self)


    def initUI(self):
    #button 
        self.librarianBtn.clicked.connect(self.librarianMode)
    
        #librarianBtn = QPushButton('Librarian Mode', self)
        #btn1.setCheckable(True)
        #btn1.setStyleSheet("QPushButton"
        #                     "{"
        #                     "background-color : rgb(255, 190, 11);"
        #                     "}"
        #                     "QPushButton::pressed"
        #                     "{"
        #                     "background-color : rgb(251, 86, 7);"
        #                     "}")
        #btn1.setGeometry(300, 300, 250, 150)
        #btn1.pressed.connect(self.librarianMode)

        #if self.camUI().isbtn12 == True:
            #btn1.hide()
        
        btn2 = QPushButton('Student Mode',self)
        btn2.setCheckable(True)
        btn2.setStyleSheet("QPushButton"
                             "{"
                             "background-color : rgb(255, 190, 11);"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : rgb(251, 86, 7);"
                             "}")
         
        btn2.pressed.connect(self.camUI)
        running = False

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)


        self.setLayout(vbox)
        self.setWindowTitle('My First Application')
        self.move(300, 300)
        self.resize(1000, 1000)
        self.show()
    


    def librarianMode(self):
        print('librarian mode')


    def camUI(self):
        print('student mode')
        global running, secondStep
        running = True
        secondStep = False
        cap = cv2.VideoCapture(0)

        while(running):
            ret, frame = cap.read()
            pub = rospy.Publisher('chatter',String,queue_size = 10)
            rospy.init_node('talker',anonymous = True)

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
                rospy.loginfo(send_str)
                pub.publish(send_str)
                rospy.sleep(0.25)

                if(barcode_data.find("2") != -1):
                    print("accepted")
                    running = False
                    QMessageBox.about(self, "Accept message", "You are accepted")
                    self.nextStep()
                else:
                   QMessageBox.about(self, "Decline message", "You are denied") 
                    
            cv2.imshow('frame',frame)       


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        #running = False
    
    def nextStep(self):

        global isbtn12
        isbtn12 = True
        print("to the next level")
        btn3 = QPushButton('Book Title', self)
        btn3.move(10, 10)
        btn3.clicked.connect(self.showDialog)

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

            # here goes the line of server stance 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #first window
    ex = MyApp()
    #second window -> book input 
    sys.exit(app.exec_())
