import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QWidget
from os import environ
import requests

def suppress_qt_warnings():
	environ["QT_DEVICE_PIXEL_RATIO"] = "0"
	environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
	environ["QT_SCREEN_SCALE_FACTORS"] = "1"
	environ["QT_SCALE_FACTOR"] = "1"

class WelcomeScreen(QDialog):
	def __init__(self):
		super(WelcomeScreen, self).__init__()
		loadUi("welcomescreen.ui",self)
		self.signin_button.clicked.connect(self.gotosignin)
		self.create_button.clicked.connect(self.gotocreate)

	def gotosignin(self):
		widget.setCurrentIndex(1)

	def gotocreate(self):
		widget.setCurrentIndex(2)

class SignInScreen(QDialog):
	def __init__(self):
		super(SignInScreen, self).__init__()
		loadUi("signinscreen.ui",self)
		self.password_box.setEchoMode(QtWidgets.QLineEdit.Password)
		self.signin_button.clicked.connect(self.signinfunction)
		self.back_button.clicked.connect(self.back)

	def back(self):
		widget.setCurrentIndex(welcomescreen_index)

	def signinfunction(self):
		user = self.username_box.text()
		password = self.password_box.text()
		print(user,password)
		
		if len(user)==0 or len(password)==0:
			self.error.setText("Please input all fields.")
		
		else:
			self.error.setText("")
			'''
			conn = sqlite3.connect("shop_data.db")
			cur = conn.cursor()
			query = 'SELECT password FROM login_info WHERE username =\''+user+"\'"
			cur.execute(query)
			result_pass = cur.fetchone()[0]
			if result_pass == password:
				print("Successfully logged in.")
				self.error.setText("")
			else:
				
			'''
			r = requests.post('https://bugtracker-api.azurewebsites.net/api/Auth', json={
			"userName": user,
			"password": password
			})
			print(f"Status Code: {r.status_code}, Response: {r.json()}")
			for i in r.json():
				print(i,":",r.json()[i])
			if r.status_code == 400:
				self.error.setText("Invalid username or password")
			elif r.status_code == 200:
				self.error.setText("")

class CreateAccScreen(QDialog):
	def __init__(self):
		super(CreateAccScreen, self).__init__()
		loadUi("createaccscreen.ui",self)
		self.password_box.setEchoMode(QtWidgets.QLineEdit.Password)
		self.confirm_password_box.setEchoMode(QtWidgets.QLineEdit.Password)
		self.signup_button.clicked.connect(self.signupfunction)
		self.back_button.clicked.connect(self.back)

	def back(self):
		widget.setCurrentIndex(0)

	def signupfunction(self):
		user = self.username_box.text()
		password = self.password_box.text()
		confirmpassword = self.confirm_password_box.text()

		if len(user)==0 or len(password)==0 or len(confirmpassword)==0:
			self.error.setText("Please fill in all inputs.")

		elif password!=confirmpassword:
			self.error.setText("Passwords do not match.")
		else:
			self.error.setText("")
		'''
		else:
			conn = sqlite3.connect("shop_data.db")
			cur = conn.cursor()

			user_info = [user, password]
			cur.execute('INSERT INTO login_info (username, password) VALUES (?,?)', user_info)

			conn.commit()
			conn.close()

			fillprofile = FillProfileScreen()
			widget.addWidget(fillprofile)
			widget.setCurrentIndex(widget.currentIndex()+1)
		'''

# before main
suppress_qt_warnings()
# main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
welcomescreen = WelcomeScreen()
widget.addWidget(welcomescreen)
welcomescreen_index = 0
signin = SignInScreen()
widget.addWidget(signin)
signin_index = 1
create = CreateAccScreen()
widget.addWidget(create)
create_index = 2

widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
#loginscreen.show()
try:
	sys.exit(app.exec())
except Exception as bug:
	print(bug)