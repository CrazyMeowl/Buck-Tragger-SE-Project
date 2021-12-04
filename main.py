import sys
import time
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QWidget,QMainWindow
from os import environ
import requests
import signin_ui
import signup_ui
import main_menu_admin_ui
import main_menu_customer_ui


def suppress_qt_warnings():
	environ["QT_DEVICE_PIXEL_RATIO"] = "0"
	environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
	environ["QT_SCREEN_SCALE_FACTORS"] = "1"
	environ["QT_SCALE_FACTOR"] = "1"
'''
class MainMenuAdmin(QDialog):
	def __init__(self):
		QDialog.__init__(self)
		loadUi("main_menu_admin.ui",self)
'''

class UserInformation():
	def __init__(self,infolist):
		self.id = infolist['id']
		self.requestAt = infolist['requestAt']
		self.expiresIn = infolist['expiresIn']
		self.accessToken = infolist['accessToken']
		self.roles = infolist['roles']
		if 'admin' in self.roles:
			print('Logged in as an Admin')
		elif 'customer' in self.roles:
			print('Logged in as a Customer')

class App():
	def __init__(self,infolist):
		self.name = infolist['name']
		self.logoURL = infolist['logoURL']
		self.companyId = infolist['companyId']
		self.id = infolist['id']

class WelcomeScreen(QDialog):
	def __init__(self):
		super(WelcomeScreen, self).__init__()
		loadUi("welcome_screen.ui",self)
		self.signin_button.clicked.connect(self.gotosignin)
		self.signup_button.clicked.connect(self.gotosignup)

	def gotosignin(self):
		widget.setCurrentIndex(signin_index)

	def gotosignup(self):
		widget.setCurrentIndex(signup_index)

class SignInScreen(QDialog):
	def __init__(self):
		super(SignInScreen, self).__init__()
		self.ui = signin_ui.Ui_Dialog()
		self.ui.setupUi(self)
		self.ui.password_box.setEchoMode(QtWidgets.QLineEdit.Password)
		self.ui.signin_button.clicked.connect(self.signinfunction)
		self.ui.back_button.clicked.connect(self.back)

	def back(self):
		widget.setCurrentIndex(welcomescreen_index)

	def signinfunction(self):
		username = self.ui.username_box.text()
		password = self.ui.password_box.text()
		#print(username,password)
		
		if len(username)==0 or len(password)==0:
			self.ui.error.setText("Please input all fields.")
		
		else:
			self.ui.error.setText("")
			r = requests.post('https://bugtracker-api.azurewebsites.net/api/Auth', json={
			"userName": username,
			"password": password
			})
			''' DEBUG Only
			print(f"Status Code: {r.status_code}, Response: {r.json()}")
			for i in r.json():
				print(i,":",r.json()[i],type(r.json()[i]))
			'''
			if r.status_code == 400:
				self.ui.error.setText("Invalid username or password")
			elif r.status_code == 200:
				user_info = UserInformation(r.json())

				if "admin" in user_info.roles:
					print("ADMIN")
					widget.setCurrentIndex(menu_admin_index)
				if "customer" in user_info.roles:
					print("Customer")
					widget.setCurrentIndex(menu_customer_index)
				#self.ui.error.setText("")


class SignUpScreen(QDialog):
	def __init__(self):
		super(SignUpScreen, self).__init__()
		self.ui = signup_ui.Ui_Dialog()
		self.ui.setupUi(self)
		self.ui.password_box.setEchoMode(QtWidgets.QLineEdit.Password)
		self.ui.confirm_password_box.setEchoMode(QtWidgets.QLineEdit.Password)
		self.ui.signup_button.clicked.connect(self.signupfunction)
		self.ui.back_button.clicked.connect(self.back)

	def back(self):
		widget.setCurrentIndex(0)

	def signupfunction(self):
		username = self.ui.username_box.text()
		password = self.ui.password_box.text()
		confirmpassword = self.ui.confirm_password_box.text()
		fullname = self.ui.fullname_box.text()
		email = self.ui.email_box.text()
		birthdate_year = self.ui.birthdate_box.date().year()
		birthdate_month = self.ui.birthdate_box.date().month()
		birthdate_date = self.ui.birthdate_box.date().day()
		#mm/dd/yyyy
		birthdate = f"{birthdate_date}/{birthdate_month}/{birthdate_year}"
		print(birthdate)
		## DEBUG ##
		#print(birthdate)
		#print(type(birthdate))

		if len(username)==0 or len(password)==0 or len(confirmpassword)==0:
			self.ui.error.setText("Please fill in all inputs.")

		elif password!=confirmpassword:
			self.ui.error.setText("Passwords do not match.")
		elif "@" not in email:
			self.ui.error.setText("Please enter a valid email.")
		else:
			self.ui.error.setText("")
			r = requests.post('https://bugtracker-api.azurewebsites.net/api/Customer/Create', json={
			"userName": username,
			"password": password,
			"fullName": fullname,
			"email": email,
			"birthdate": birthdate
			})
			print(r)
			print(f"Status Code: {r.status_code}, Response: {r.json()}")
			for i in r.json():
				print(i,":",r.json()[i],type(r.json()[i]))
			if r.status_code == 400:
				self.ui.error.setText("Username was taken.")
			elif r.status_code == 200:
				self.ui.error.setText("You shouldn't see this line, or should you?")
				#widget.hide()

class MainMenuAdminScreen(QDialog):
	def __init__(self):
		super(MainMenuAdminScreen, self).__init__()
		self.ui = main_menu_admin_ui.Ui_Dialog()
		self.ui.setupUi(self)

class MainMenuCustomerScreen(QDialog):
	def __init__(self):
		super(MainMenuCustomerScreen, self).__init__()
		self.side_menu_state = False

		self.ui = main_menu_customer_ui.Ui_Dialog()
		self.ui.setupUi(self)

		self.ui.slide_menu_container.setMaximumWidth(0)
		self.ui.exit_button.clicked.connect(exit)
		self.ui.menu_button.clicked.connect(self.trigger_side_menu)
		self.ui.refresh_button.clicked.connect(self.reload_app_list)
		self.ui.search_button.clicked.connect(self.search_for_app)
		self.app_list = []
		self.load_app_list()

	def clear_app_list(self):
		self.app_list = []
		self.ui.app_list.clear()

	def search_for_app(self):
		self.clear_app_list()
		keyword = self.ui.search_box.text()
		link = 'https://bugtracker-api.azurewebsites.net/api/App/SearchByName/'
		r = requests.get(link+keyword)
		for i in r.json():
			self.app_list.append(App(i))
		for a in self.app_list:
			self.ui.app_list.addItem(a.name)

	def reload_app_list(self):
		self.clear_app_list()
		self.load_app_list()
		
	def load_app_list(self):
		self.app_list = []
		r = requests.get('https://bugtracker-api.azurewebsites.net/api/App/GetAll')
		for i in r.json():
			self.app_list.append(App(i))
		for a in self.app_list:
			self.ui.app_list.addItem(a.name)
		'''
		i = 0
		while i < 100:
			self.ui.app_list.addItem(str(i))
			i = i + 1
		'''
	def trigger_side_menu(self):
		
		if self.side_menu_state == False:
			self.ui.slide_menu_container.setMaximumWidth(250)
		else:
			self.ui.slide_menu_container.setMaximumWidth(0)
		self.side_menu_state = not self.side_menu_state
		
	def add_it(self):


			# Grab the item from the list box
			item = self.additem_lineEdit.text()

			# Add item to list
			self.mylist_listWidget.addItem(item)

			# Clear the item box
			self.additem_lineEdit.setText("")
# before main
if __name__ == "__main__":
	suppress_qt_warnings()
	# main
	app = QApplication(sys.argv)
	widget = QtWidgets.QStackedWidget()

	welcomescreen = WelcomeScreen()
	widget.addWidget(welcomescreen)
	welcomescreen_index = 0

	signinscreen = SignInScreen()
	widget.addWidget(signinscreen)
	signin_index = 1

	signupscreen = SignUpScreen()
	widget.addWidget(signupscreen)
	signup_index = 2

	mainmenuadminscreen = MainMenuAdminScreen()
	widget.addWidget(mainmenuadminscreen)
	menu_admin_index = 3

	mainmenucustomerscreen = MainMenuCustomerScreen()
	widget.addWidget(mainmenucustomerscreen)
	menu_customer_index = 4

	widget.setFixedHeight(800)
	widget.setFixedWidth(1200)
	widget.show()
	#loginscreen.show()
	try:
		sys.exit(app.exec())
	except Exception as bug:
		print(bug)