import sys
import requests, json 
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
import rospy 
from std_msgs.msg import String
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QInputDialog, QVBoxLayout, QMessageBox

class WelcomeScreen(QDialog):

    running = False
    isbtn12 = False
    ok = False
    isPhase4 = False
    
    def __init__(self):
        super(WelcomeScreen,self).__init__()
        loadUi("welcomescreen.ui",self)
        print("loaded")
        self.LibrarianBtn.clicked.connect(self.librarianMode)
        self.StudentBtn.clicked.connect(self.StudentMode)


    def librarianMode(self):
        print("hello library")
        #whatever it is .. 
        #barcode 
        global running, secondStep, ok, count
        # running = True
        # secondStep = False
        count = 0
        
        option = QtWidgets.QMessageBox.question(self, "QMessageBox", "Do you want to register your books?", QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Yes)
        if option == QtWidgets.QMessageBox.Yes : 
            self.decodedValue()

    def decodedValue(self):

        global running, secondStep, ok, count
        running = True
        cap = cv2.VideoCapture(0)
            
        while(running):
            ret, frame = cap.read()
            #pub = rospy.Publisher('chatter',String,queue_size = 10)
            #rospy.init_node('talker',anonymous = True)

            if not ret:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            decoded = pyzbar.decode(gray)
            #print(type(decoded))
            #print(decoded)
            
            
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
                data = {"bookBarcodeInfo": barcode_data} 
                URL = 'http://1.232.197.66:3000/bookTakeoutRequest'
                res = requests.post(URL, data=json.dumps(data))
                print(res.json())
                print(send_str)
                
                option = QtWidgets.QMessageBox.question(self, "QMessageBox", "Do you want to register more books?", QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Yes)
                if option == QtWidgets.QMessageBox.Yes:       
                    running = False
                    print("out")
                    
                elif option ==  QtWidgets.QMessageBox.No: 
                    running = False
                    phase3n2 = phaseThree2()
                    widget.addWidget(phase3n2)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                    isPhase4 = False
                    
            cv2.imshow('frame',frame)       
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        running = False


    def StudentMode(self):
        print("hello student")
        self.cv2Show()

    def cv2Show(self):
        global running, secondStep, isPhase4
        running = True
        secondStep = False
        isPhase4 = False
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
                data = {"barcode_data": barcode_data} 
                URL = 'http://1.232.197.66:3000/studentInfo'
                res = requests.post(URL, data=json.dumps(data))
                print(res.json())

                if(barcode_data.find("2") != -1):
                    print("accepted")
                    running = False
                    QMessageBox.about(self, "Accept message", "You are accepted")
                    #self.BookEnter()
                    phase2 = phaseTwo()
                    widget.addWidget(phase2)
                    widget.setCurrentIndex(widget.currentIndex()+1)

                else:
                   QMessageBox.about(self, "Decline message", "You are denied") 
                    
            cv2.imshow('frame',frame)       


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        running = False
#student
#entering book title
class phaseTwo(QDialog):

    def __init__(self):
        super(phaseTwo,self).__init__()
        loadUi("phase2.ui",self)

        self.bookinputfield.textChanged.connect(self.lineeditTextFunction)
        self.bookinputfield.returnPressed.connect(self.printTextFunction)
        self.bookEnter.clicked.connect(self.showmsgs)
    
    def lineeditTextFunction(self):
        self.Outputlabel.setText(self.bookinputfield.text())

    def printTextFunction(self):
        #get the name of the book 
        data = {"bookInfo": self.bookinputfield.text()} 
        URL = 'http://1.232.197.66:3000/bookInfo'
        res = requests.post(URL, data=json.dumps(data))
        print(res.json())
        print(self.bookinputfield.text())

    def showmsgs(self):
        QMessageBox.about(self, "Finding path", "Robot is finding path")

        phase3 = phaseThree()
        widget.addWidget(phase3)
        widget.setCurrentIndex(widget.currentIndex()+1)

#librarian
#robot is finding path continue to welcome
class phaseThree2(QDialog):

    def __init__(self):
        super(phaseThree2, self).__init__()
        loadUi("phase3.ui",self)
        self.progressBar.valueChanged.connect(self.printValue)

        self.timerVar = QTimer()
        self.timerVar.setInterval(100)
        self.timerVar.timeout.connect(self.progressBarTimer)
        self.timerVar.start()

    def progressBarTimer(self) :
        self.time = self.progressBar.value()
        self.time += 1
        self.progressBar.setValue(self.time)

        if self.time >= self.progressBar.maximum() :
            self.timerVar.stop()
            QMessageBox.about(self, "Finding path", "Here is the destination")
            
            welcome = WelcomeScreen()
            widget.addWidget(welcome)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def printValue(self) :
        print(self.progressBar.value())

#student
#robot is finding path continue to phase4 
class phaseThree(QDialog):
    global isPhase4

    def __init__(self):
        super(phaseThree, self).__init__()
        loadUi("phase3.ui",self)
        self.progressBar.valueChanged.connect(self.printValue)

        self.timerVar = QTimer()
        self.timerVar.setInterval(100)
        self.timerVar.timeout.connect(self.progressBarTimer)
        self.timerVar.start()

    def progressBarTimer(self) :
        self.time = self.progressBar.value()
        self.time += 1
        self.progressBar.setValue(self.time)

        if self.time >= self.progressBar.maximum() :
            self.timerVar.stop()
            QMessageBox.about(self, "Finding path", "Here is the destination")
            
            isPhase4 = True
            if isPhase4 : 
                phase4 = phaseFour()
                widget.addWidget(phase4)
                widget.setCurrentIndex(widget.currentIndex()+1)


    def printValue(self) :
        print(self.progressBar.value())

#student
#get the title of the book
class phaseFour(QDialog):

    cv2running = False
    count = 0

    def __init__(self):
        super(phaseFour,self).__init__()
        loadUi("phase4.ui",self)
        self.cvPush.clicked.connect(self.cv2show2)
    
    def cv2show2(self):
        ok = False
        global cv2running, barcode_data
        cv2running= True
        cap = cv2.VideoCapture(0)

        while(cv2running):
            ret, frame = cap.read()

            if not ret:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            decoded = pyzbar.decode(gray)
            
            for d in decoded:
                x,y,w,h = d.rect
                barcode_data = d.data.decode("utf-8")
                barcode_type = d.type
                cv2.rectangle(frame,(x,y),(x+w,y+h), (0,0,255),2)
                text='%s(%s)'%(barcode_data, barcode_type)
                cv2.putText(frame,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2,cv2.LINE_AA)
                send_str = barcode_data

                data = {"bookBarcodeInfo": barcode_data} 
                URL = 'http://1.232.197.66:3000/bookBarcodeInfo'
                res = requests.post(URL, data=json.dumps(data))
                print(res.json())

                if(barcode_data.find("2") != -1):
                    print("accepted")
                    #count +=1
                    #if(count > 4) :
                    cv2running = False
                    QMessageBox.about(self, "Finished scanning", "Finished scanning")
                    ok = True
                    if ok :
                        self.backtowelcome()

                    
            cv2.imshow('frame',frame)       

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        running = False
    
    def backtowelcome(self):

        data = {"bookBarcodeInfo": barcode_data} 
        URL = 'http://1.232.197.66:3000/bookTakeoutRequest'
        res = requests.post(URL, data=json.dumps(data))
        print(res.json())

        QMessageBox.about(self, "Alert message", "Finished checking out")
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)


# main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")