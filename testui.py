from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow
import sys
from os import environ

#Skip the QT Warnings
def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

suppress_qt_warnings()


class firstWindow(QMainWindow):
	def __init__(self):
		super(firstWindow,self).__init__()
		#window size
		self.setGeometry(100,100,1600,900)
		#title
		self.setWindowTitle("Title")
		self.initUI()

	def initUI(self):
		#text	
		self.label = QtWidgets.QLabel(self)
		self.label.setText("Testing Text!")
		self.label.move(100,100)
		

		#button
		self.b1 = QtWidgets.QPushButton(self)
		self.b1.setText("Click me")
		self.b1.clicked.connect(lambda: self.clicked())
	
	#test clicked funtion ( method )
	def clicked(self):
		self.label.setText("You clicked")
		self.update()

	def update(self):
		#update size for text label
		self.label.adjustSize()


#the window function
def window():
	#initialize
	app = QApplication(sys.argv)
	win = firstWindow()

	win.show()
	sys.exit(app.exec_())

window()
