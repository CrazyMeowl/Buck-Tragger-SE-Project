try:
	import sys
	import time
	from PyQt5 import QtGui
	from PyQt5.uic import loadUi
	from PyQt5 import QtWidgets
	from PyQt5.QtWidgets import QDialog,QApplication,QWidget,QMainWindow,QMessageBox
	from PyQt5.QtCore import QDate
	from os import environ
	import requests
	import signin_ui
	import signup_ui
	import main_menu_admin_ui
	import main_menu_customer_ui
	import main_menu_staff_ui
	import report_ui
	import popup_ui
	import welcome_ui
	import webbrowser

	#mandatory
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
	def popupmessage(inTitle,inText):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setWindowTitle(inTitle)
		msg.setWindowIcon(QtGui.QIcon('logo.png'))
		msg.setText(inText)
		msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		retval = msg.exec_()
		if retval == QMessageBox.Yes:
			return True
		elif retval == QMessageBox.No:
			return False
	class User():
		def __init__(self):
			self.id = 0
			self.requestAt = 0
			self.expiresIn = 0
			self.accessToken = 0
			self.roles = 0
		def updateData(self,infolist):
			self.id = infolist['id']
			self.requestAt = infolist['requestAt']
			self.expiresIn = infolist['expiresIn']
			self.accessToken = infolist['accessToken']
			self.roles = infolist['roles']
		def signout(self):
			self.id = 0
			self.requestAt = 0
			self.expiresIn = 0
			self.accessToken = 0
			self.roles = 0
	class Staff():
		def __init__(self,infolist):
			self.userName = infolist['userName']
			self.fullName = infolist['fullName']
			self.companyId = infolist['companyId']
			self.email = infolist['email']
			self.id = infolist['id']
	class App():
		def __init__(self,infolist):
			self.name = infolist['name']
			self.logoURL = infolist['logoURL']
			self.companyId = infolist['companyId']
			self.id = infolist['id']

	class Report():
		def __init__(self,infolist):
			self.title = infolist['title']
			self.description = infolist['description']
			self.appId = infolist['appId']
			self.id = infolist['id']

	class Bug():
		def __init__(self,infolist):
			self.title = infolist['title']
			self.serverity = infolist["serverity"]
			self.status = infolist["status"]
			self.description = infolist['description']
			self.appId = infolist['appId']
			self.id = infolist['id']
			self.serverities_list = ["Small","Normal","Bad","Extreme","EMERGENCY"]
			self.status_list = ["Working","Fixed","Revised","Approved"]

	class WelcomeScreen(QDialog):
		def __init__(self):
			super(WelcomeScreen, self).__init__()
			self.ui = welcome_ui.Ui_Dialog()
			self.ui.setupUi(self)
			self.ui.signin_button.clicked.connect(self.gotosignin)
			self.ui.signup_button.clicked.connect(self.gotosignup)

		def gotosignin(self):
			widget.setCurrentIndex(signin_index)

		def gotosignup(self):
			widget.setCurrentIndex(signup_index)

	user = User()
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
					a = r.json()
					print(r.json())
					user.updateData(a)
					if "staff" in user.roles:
						#print("ADMIN")
						print("hello")
						widget.setCurrentIndex(menu_staff_index)
						mainmenustaffscreen.load_app_list()
					if "admin" in user.roles:
						#print("ADMIN")
						widget.setCurrentIndex(menu_admin_index)
						mainmenuadminscreen.load_app_staff_list()
					if "customer" in user.roles:
						#print("Customer")
						widget.setCurrentIndex(menu_customer_index)
					self.ui.username_box.clear()
					self.ui.password_box.clear()
					#self.ui.error.setText("")

	class PopupScreen(QDialog):
		def __init__(self):
			super(PopupScreen, self).__init__()
			self.ui = popup_ui.Ui_Dialog()
			self.ui.setupUi(self)
			self.ui.email_button.clicked.connect(self.open_email)
			self.setWindowTitle("Create Company Ui")
			self.setWindowIcon(QtGui.QIcon('logo.png'))

		def open_email(self):
			recipient = 'ITITIU19185@student.hcmiu.edu.vn'
			subject = 'Create Company Request'
			body = 'Hello im ... Owner of ... . I would like to create a company on your BugTracker app'
			body = body.replace(' ', '%20')
			webbrowser.open('mailto:?to=' + recipient + '&subject=' + subject + '&body=' + body, new=1)

	class SignUpScreen(QDialog):
		def __init__(self):
			super(SignUpScreen, self).__init__()
			self.ui = signup_ui.Ui_Dialog()
			self.ui.setupUi(self)
			self.ui.password_box.setEchoMode(QtWidgets.QLineEdit.Password)
			self.ui.confirm_password_box.setEchoMode(QtWidgets.QLineEdit.Password)
			self.ui.signup_button.clicked.connect(self.signupfunction)
			self.ui.back_button.clicked.connect(self.back)
			self.ui.create_company_button.clicked.connect(self.popupemail)
			self.date = QDate.currentDate()
			self.ui.birthdate_box.setDate(self.date)

		def popupemail(self):
			self.popupscreen = PopupScreen()
			#self.popupscreen.setFixedHeight(800)
			#self.popupscreen.setFixedWidth(1200)
			self.popupscreen.raise_()
			self.popupscreen.show()

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
			birthdate = f"{birthdate_date}/{birthdate_month}/{birthdate_year}"
			print(birthdate)
			if len(username)==0 or len(password)==0 or len(confirmpassword)==0:
				self.ui.error.setText("Please fill in all inputs.")

			elif password!=confirmpassword:
				self.ui.error.setText("Passwords do not match.")
			elif "@" not in email:
				self.ui.error.setText("Please enter a valid email.")
			elif ' ' in username:
				self.ui.error.setText("Please remove space from your username.")
			else:
				self.ui.error.setText("")
				r = requests.post('https://bugtracker-api.azurewebsites.net/api/Customer/Create', json={
				"userName": username,
				"password": password,
				"fullName": fullname,
				"email": email,
				"birthdate": birthdate
				})
				#print(r)
				# for debug
				#print(f"Status Code: {r.status_code}, Response: {r.json()}")
				#for i in r.json():
				#	print(i,":",r.json()[i],type(r.json()[i]))
				if r.status_code == 400 or r.status_code == 500:
					self.ui.error.setText("Username was taken.")
				else:
					self.ui.error.setText("You shouldn't see this line, or should you?")
					widget.setCurrentIndex(menu_customer_index)
					self.ui.username_box.clear()
					self.ui.password_box.clear()
					self.ui.confirm_password_box.clear()
					self.ui.fullname_box.clear()
					self.ui.email_box.clear()
					self.ui.birthdate_box.setDate(self.date)
	#Admin
	class MainMenuAdminScreen(QDialog):
		def __init__(self):
			super(MainMenuAdminScreen, self).__init__()
			self.side_menu_state = False
			self.itemSelectionDetected = False
			self.ui = main_menu_admin_ui.Ui_Dialog()
			self.ui.setupUi(self)

			self.ui.slide_menu_container.setMaximumWidth(0)

			self.ui.exit_button.clicked.connect(sys.exit)

			self.ui.menu_button.clicked.connect(self.trigger_side_menu)

			self.ui.refresh_button.clicked.connect(self.reload_list)

			self.ui.app_list.itemClicked.connect(self.clicked_on_app_list)

			self.ui.staff_list.itemClicked.connect(self.clicked_on_staff_list)

			self.ui.update_app_button.clicked.connect(self.show_update_app_page)

			self.ui.back_to_info_app_page.clicked.connect(self.show_app_info_page)

			self.ui.update_staff_button.clicked.connect(self.load_staff_info_to_update)

			self.ui.update_staff_password_box.setEchoMode(QtWidgets.QLineEdit.Password)

			self.ui.create_staff_password_box.setEchoMode(QtWidgets.QLineEdit.Password)

			self.ui.cancel_create_staff_button.clicked.connect(self.show_welcome_page)

			self.ui.cancel_update_staff_button.clicked.connect(self.show_staff_info_page)

			self.password_mode_update = True

			self.password_mode_create = True

			self.ui.update_staff_show_password_button.clicked.connect(self.trigger_password_mode_update)

			self.ui.create_staff_show_password_button.clicked.connect(self.trigger_password_mode_create)

			self.ui.confirm_update_staff_button.clicked.connect(self.update_staff)
			#self.ui.app_list.itemClicked.connect(self.show_app_page)
			#self.ui.report_list.itemClicked.connect(lambda: self.load_report_info("new"))

			self.ui.website_button.clicked.connect(self.open_link)

			self.ui.email_button.clicked.connect(self.open_email)

			self.ui.app_list.itemSelectionChanged.connect(self.on_change_app)

			self.ui.signout_button.clicked.connect(self.signout)

			self.ui.update_staff_show_password_button.hide()

			self.app_list = []
			self.staff_list = []
			self.add_id = None
			self.companyId = None
			self.info_app_staff_list = []
		def trigger_password_mode_update(self):
			if self.password_mode_update :
				self.password_mode_update = False
				self.ui.update_staff_password_box.setEchoMode(QtWidgets.QLineEdit.Normal)	
			else:
				self.password_mode_update = True
				self.ui.update_staff_password_box.setEchoMode(QtWidgets.QLineEdit.Password)
		
		def trigger_password_mode_create(self):
			if self.password_mode_create:
				self.password_mode_create = False
				self.ui.create_staff_password_box.setEchoMode(QtWidgets.QLineEdit.Normal)
			else:
				self.password_mode_create = True
				self.ui.create_staff_password_box.setEchoMode(QtWidgets.QLineEdit.Password)
		def signout(self):
			user.signout()
			self.clear_all_list()
			widget.setCurrentIndex(welcomescreen_index)

		def clicked_on_app_list(self):
			#print(self.ui.app_list.currentItem().text())
			if self.ui.app_list.currentItem().text() == 'Create New App...':
				self.show_create_app_page()
			else:
				self.load_app_info()

		def clicked_on_staff_list(self):
			#print(self.ui.app_list.currentItem().text())
			if self.ui.staff_list.currentItem().text() == 'Create New Staff...':
				self.show_create_staff_page()
			else:
				self.load_staff_info()
		


		def load_staff_info(self):
			self.show_staff_info_page()
			leStaff = self.staff_list[self.ui.staff_list.currentRow()]
			self.ui.info_staff_username_box.setText(leStaff.userName)
			self.ui.info_staff_fullname_box.setText(leStaff.fullName)
			self.ui.info_staff_email_box.setText(leStaff.email)

		def load_staff_info_to_update(self):
			self.show_update_staff_page()
			leStaff = self.staff_list[self.ui.staff_list.currentRow()]
			self.ui.update_staff_username_box.setText(leStaff.userName)
			self.ui.update_staff_fullname_box.setText(leStaff.fullName)
			self.ui.update_staff_email_box.setText(leStaff.email)
			


		def update_staff(self):
			leStaff = self.staff_list[self.ui.staff_list.currentRow()]
			userName = self.ui.update_staff_username_box.text()
			fullName = self.ui.update_staff_fullname_box.text()
			email = self.ui.update_staff_email_box.text()
			password = self.ui.update_staff_password_box.text()
			staffId = leStaff.id
			companyId = leStaff.companyId
			if popupmessage("Caution!!!","Are you sure you want to update this staff information ???"):
				r = requests.put('https://bugtracker-api.azurewebsites.net/api/Staff/Update', json={
				"id": staffId,
				"userName" : userName,
				"password" : password,
				"fullName" : fullName,
				"companyId": companyId,
				"email" : email
				})
			print(r)
			self.show_welcome_page()
			self.reload_list()
			#print(r.json())

		def load_app_info(self):
			self.show_app_info_page()

			leApp = self.app_list[self.ui.app_list.currentRow()]
			self.ui.info_app_name_box.setText(leApp.name)
			#self.ui.create_app_logoUrl_box.setText(leApp.logoURL)
			self.info_app_staff_list = []
			self.ui.info_app_staff_list.clear()
			r = requests.get('https://bugtracker-api.azurewebsites.net/api/Staff/GetByAppId/'+str(leApp.id))
			for i in r.json():
				self.info_app_staff_list.append(Staff(i))
				#print(i)
			for s in self.staff_list:
				self.ui.info_app_staff_list.addItem(s.userName)

		def show_welcome_page(self):
			self.ui.pager.setCurrentIndex(0)
		
		def show_app_info_page(self):
			self.ui.pager.setCurrentIndex(1)

		def show_create_app_page(self):
			self.ui.pager.setCurrentIndex(2)

		def show_update_app_page(self):
			self.ui.pager.setCurrentIndex(3)

		def show_staff_info_page(self):
			self.ui.pager.setCurrentIndex(4)

		def show_update_staff_page(self):
			self.ui.pager.setCurrentIndex(5)

		def show_create_staff_page(self):
			self.ui.pager.setCurrentIndex(6)

		

		def on_change_app(self):
			#self.show_app_page(	)
			self.itemSelectionDetected = True
			#print("nice")
			
		def open_email(self):
			recipient = 'ITITIU19185@student.hcmiu.edu.vn'
			subject = 'Need support'
			body = 'Hello im ... i need a support to help me with ... . I have '
			body = body.replace(' ', '%20')
			webbrowser.open('mailto:?to=' + recipient + '&subject=' + subject + '&body=' + body, new=1)

		def open_link(self):
			webbrowser.open("https://bugtracker-api.azurewebsites.net/swagger/index.html")

		def clear_app_list(self):
			self.app_list = []
			self.ui.app_list.clear()

		def clear_all_list(self):
			self.app_list = []
			self.ui.app_list.clear()
			self.staff_list = []
			self.ui.staff_list.clear()
			self.companyId = None

		def reload_list(self):
			self.clear_app_list()
			self.ui.staff_list.clear()
			self.staff_list = []
			self.load_app_staff_list()
			self.itemSelectionDetected = False
			
		def load_app_staff_list(self):
			self.app_list = []
			self.staff_list = []
			r = requests.get('https://bugtracker-api.azurewebsites.net/api/Company/GetAll')
			print(r.json())
			for c in r.json():
				if c['adminId'] == user.id:
					companyId = c['id']
					r = requests.get('https://bugtracker-api.azurewebsites.net/api/App/GetByCompanyId/'+str(companyId))
					for i in r.json():
						self.app_list.append(App(i))
						print(i)
					for a in self.app_list:
						self.ui.app_list.addItem(a.name)

					rr = requests.get('https://bugtracker-api.azurewebsites.net/api/Staff/GetByCompanyId/'+str(companyId))
					for ii in rr.json():
						self.staff_list.append(Staff(ii))
						#print(i)
					for s in self.staff_list:
						self.ui.staff_list.addItem(s.userName)

			self.ui.staff_list.addItem("Create New Staff...")
			self.ui.app_list.addItem("Create New App...")

		def trigger_side_menu(self):
			if self.side_menu_state == False:
				self.ui.slide_menu_container.setMaximumWidth(250)
			else:
				self.ui.slide_menu_container.setMaximumWidth(0)
			self.side_menu_state = not self.side_menu_state
			

	#staff
	class MainMenuStaffScreen(QDialog):
		def __init__(self):
			super(MainMenuStaffScreen, self).__init__()
			self.side_menu_state = False
			self.itemSelectionDetected = False
			self.ui = main_menu_staff_ui.Ui_Dialog()
			self.ui.setupUi(self)

			self.ui.slide_menu_container.setMaximumWidth(0)
			self.ui.exit_button.clicked.connect(sys.exit)
			self.ui.menu_button.clicked.connect(self.trigger_side_menu)
			self.ui.refresh_button.clicked.connect(self.reload_app_list)
			#self.ui.search_button.clicked.connect(self.search_for_app)
			#self.ui.report_button.clicked.connect(self.report_app)
			self.ui.app_list.itemClicked.connect(self.load_report_bug)
			self.ui.app_list.itemClicked.connect(self.show_app_page)
			self.ui.report_list.itemClicked.connect(lambda: self.load_report_info("new"))

			self.ui.old_report_list.itemClicked.connect(lambda: self.load_report_info("old"))
			#self.ui.report_list.itemDoubleClicked.connect(self.load_report_info)
			self.ui.bug_list.itemClicked.connect(self.load_bug_info)
			#self.ui.bug_list.itemDoubleClicked.connect(self.load_bug_info)
			self.ui.website_button.clicked.connect(self.open_link)

			self.ui.email_button.clicked.connect(self.open_email)

			self.ui.app_list.itemSelectionChanged.connect(self.on_change_app)

			self.ui.signout_button.clicked.connect(self.signout)

			self.ui.create_bug_button.clicked.connect(self.load_report_to_bug)

			self.ui.update_bug_button.clicked.connect(self.load_bug_to_update)

			self.ui.cancel_create_bug_button.clicked.connect(self.show_report_page)

			self.ui.cancel_update_bug_button.clicked.connect(self.show_bug_page)

			self.ui.confirm_create_bug_button.clicked.connect(self.create_bug)

			self.ui.confirm_update_bug_button.clicked.connect(self.update_bug)

			self.ui.delete_report_button.clicked.connect(self.delete_report)

			self.ui.delete_bug_button.clicked.connect(self.delete_bug)

			self.app_list = []
			self.report_list = []
			self.old_report_list = []
			self.bug_list = []
			self.add_id = None
			#self.load_app_list()
		def create_bug(self):
			if popupmessage("Caution!!!","Are you sure you want to create this bug ???"):
				#print("Created")
				serverity = self.ui.create_bug_serverity_box.currentIndex()
				status = self.ui.create_bug_status_box.currentIndex()
				title = self.ui.create_bug_title_box.toPlainText()
				desc = self.ui.create_bug_description_box.toPlainText()
				app_id = self.app_list[self.ui.app_list.currentRow()].id
				report_id = self.report_list[self.ui.report_list.currentRow()].id
				report_list = [report_id]
				r = requests.post('https://bugtracker-api.azurewebsites.net/api/Bug/Create', json={
				"id": 0,
				"title": title,
				"serverity": serverity,
				"status": status,
				"description": desc,
				"appId": app_id,
				"reportIDs": report_list
				})
				#print(r)

				'''
				{
				  "id": 0,
				  "title": "string",
				  "serverity": 0,
				  "status": 0,
				  "description": "string",
				  "appId": 1,
				  "reportIDs": [
				    1
				  ]
				}
				'''
				self.reload_app_list()
		def update_bug(self):
			if popupmessage("Caution!!!","Are you sure you want to update this bug ???"):

				serverity = self.ui.update_bug_serverity_box.currentIndex()
				status = self.ui.update_bug_status_box.currentIndex()
				title = self.ui.update_bug_title_box.toPlainText()
				desc = self.ui.update_bug_description_box.toPlainText()
				print(desc)
				app_id = self.app_list[self.ui.app_list.currentRow()].id
				bug_id = self.bug_list[self.ui.bug_list.currentRow()].id
				#report_list = []
				r = requests.put('https://bugtracker-api.azurewebsites.net/api/Bug/Update', json={
				
				"title": title,
				"serverity": serverity,
				"status": status,
				"description": desc,
				"appId": app_id,
				"id": bug_id
				})
				self.reload_app_list()
				

		def delete_report(self):
			if popupmessage("Caution!!!","Are you sure you want to delete this report ???"):
				leReport = self.report_list[self.ui.report_list.currentRow()]
				r = requests.delete('https://bugtracker-api.azurewebsites.net/api/Report/Delete/'+str(leReport.id))
				self.reload_app_list()


		def delete_bug(self):
			related_report_list = []
			if popupmessage("Caution!!!","Are you sure you want to delete this bug ???"):
				leBug = self.bug_list[self.ui.bug_list.currentRow()]
				r = requests.get('https://bugtracker-api.azurewebsites.net/api/Report/GetByBugId/'+str(leBug.id))
				for i in r.json():
					leReport = Report(i)
					r = requests.delete('https://bugtracker-api.azurewebsites.net/api/Report/Delete/'+str(leReport.id))
				r2 = requests.delete('https://bugtracker-api.azurewebsites.net/api/Bug/Delete/'+str(leBug.id))
				self.reload_app_list()

		def show_app_page(self):
			self.ui.pager.setCurrentIndex(0)

		def show_report_page(self):
			self.ui.pager.setCurrentIndex(1)

		def show_bug_page(self):
			self.ui.pager.setCurrentIndex(2)

		def show_update_bug_page(self):
			self.ui.pager.setCurrentIndex(3)

		def show_create_bug_page(self):
			self.ui.pager.setCurrentIndex(4)

		def load_bug_to_update(self):
			self.show_update_bug_page()
			leBug = self.bug_list[self.ui.bug_list.currentRow()]
			self.ui.update_bug_title_box.setPlainText(leBug.title)
			self.ui.update_bug_description_box.setPlainText(leBug.description)

		def load_report_to_bug(self):
			self.show_create_bug_page()
			leReport = self.report_list[self.ui.report_list.currentRow()]
			self.ui.create_bug_title_box.setPlainText(leReport.title)
			self.ui.create_bug_description_box.setPlainText("""Date : \nTested by :\nCause by :\nDesc on report: """)
			self.ui.create_bug_description_box.appendPlainText(leReport.description)	

		def load_report_info(self,inString):
			self.show_report_page()
			if inString == 'new':
				leReport = self.report_list[self.ui.report_list.currentRow()]
				self.ui.create_bug_button.show()
				self.ui.delete_report_button.show()
			elif inString == 'old':
				leReport = self.old_report_list[self.ui.old_report_list.currentRow()]
				self.ui.delete_report_button.hide()
				self.ui.create_bug_button.hide()

			self.ui.report_title_box.setPlainText(leReport.title)
			self.ui.report_description_box.setPlainText(leReport.description)	
		def load_bug_info(self):
			self.show_bug_page()
			leBug = self.bug_list[self.ui.bug_list.currentRow()]
			self.ui.bug_title_box.setPlainText(leBug.title)
			self.ui.bug_description_box.setPlainText(leBug.description)
			self.ui.bug_status_box.setPlainText(leBug.status_list[leBug.status])
			self.ui.bug_serverity_box.setPlainText(leBug.serverities_list[leBug.serverity])
			#there is a color function needed to be done

		def load_report_bug(self):
			self.app_id = self.app_list[self.ui.app_list.currentRow()].id
			print(self.app_id)
			self.ui.side_box.setCurrentIndex(1)
			self.report_list = []
			self.old_report_list = []
			self.ui.old_report_list.clear()
			self.ui.report_list.clear()

			r = requests.get('https://bugtracker-api.azurewebsites.net/api/Report/GetByAppId/'+str(self.app_id))
			for i in r.json():
				leReport = Report(i)
				rr = requests.get('https://bugtracker-api.azurewebsites.net/api/Bug/GetByReportId/'+str(leReport.id))
				if rr.status_code == 200:
					self.old_report_list.append(leReport)
				elif rr.status_code == 204:
					self.report_list.append(leReport)

			#https://bugtracker-api.azurewebsites.net/api/Bug/GetByReportId/5

			for n in self.report_list:
				self.ui.report_list.addItem(n.title)

			for o in self.old_report_list:
				self.ui.old_report_list.addItem(o.title)

			self.bug_list = []
			self.ui.bug_list.clear()

			r = requests.get('https://bugtracker-api.azurewebsites.net/api/Bug/GetByAppId/'+str(self.app_id))
			for i in r.json():
				self.bug_list.append(Bug(i))
			for a in self.bug_list:
				self.ui.bug_list.addItem(a.title)

		def signout(self):
			user.signout()
			self.clear_all_list()
			widget.setCurrentIndex(welcomescreen_index)
		def on_change_app(self):
			self.show_app_page()
			self.itemSelectionDetected = True
			#print("nice")
			
		def open_email(self):
			recipient = 'ITITIU19185@student.hcmiu.edu.vn'
			subject = 'Need support'
			body = 'Hello im ... i need a support to help me with ... . I have '
			body = body.replace(' ', '%20')
			webbrowser.open('mailto:?to=' + recipient + '&subject=' + subject + '&body=' + body, new=1)

		def open_link(self):
			webbrowser.open("https://bugtracker-api.azurewebsites.net/swagger/index.html")

		def clear_app_list(self):
			self.app_list = []
			self.ui.app_list.clear()

		def clear_all_list(self):
			self.app_list = []
			self.ui.app_list.clear()
			self.report_list = []
			self.ui.report_list.clear()
			self.bug_list = []
			self.ui.bug_list.clear()
			self.old_report_list = []
			self.ui.old_report_list.clear()

		def reload_app_list(self):
			self.clear_app_list()
			self.load_app_list()
			self.repot_list = []
			self.ui.report_list.clear()
			self.bug_list = []
			self.ui.bug_list.clear()
			self.itemSelectionDetected = False
			
		def load_app_list(self):
			self.app_list = []
			r = requests.get('https://bugtracker-api.azurewebsites.net/api/App/GetByStaffId/'+user.id)
			for i in r.json():
				self.app_list.append(App(i))
				print(i)
			for a in self.app_list:
				self.ui.app_list.addItem(a.name)
			'''
			i = 0
			while i < 100:
				self.ui.app_list.addItem(str(i))
				i = i + 1
			'''
			#print(user.id)
		def trigger_side_menu(self):
			if self.side_menu_state == False:
				self.ui.slide_menu_container.setMaximumWidth(250)
			else:
				self.ui.slide_menu_container.setMaximumWidth(0)
			self.side_menu_state = not self.side_menu_state
	#customer
	class MainMenuCustomerScreen(QDialog):
		def __init__(self):
			super(MainMenuCustomerScreen, self).__init__()
			self.side_menu_state = False
			self.itemSelectionDetected = False
			self.ui = main_menu_customer_ui.Ui_Dialog()
			self.ui.setupUi(self)

			self.ui.slide_menu_container.setMaximumWidth(0)
			self.ui.exit_button.clicked.connect(sys.exit)
			self.ui.menu_button.clicked.connect(self.trigger_side_menu)
			self.ui.refresh_button.clicked.connect(self.reload_app_list)
			self.ui.search_button.clicked.connect(self.search_for_app)
			self.ui.report_button.clicked.connect(self.report_app)
			self.ui.website_button.clicked.connect(self.open_link)
			self.ui.email_button.clicked.connect(self.open_email)
			self.ui.app_list.itemSelectionChanged.connect(self.on_change_app_app)
			self.ui.signout_button.clicked.connect(self.signout)
			self.app_list = []
			self.load_app_list()
		def signout(self):
			user.signout()
			widget.setCurrentIndex(welcomescreen_index)
		def on_change_app_app(self):
			self.itemSelectionDetected = True
				
		def open_email(self):
			recipient = 'ITITIU19185@student.hcmiu.edu.vn'
			subject = 'Need support'
			body = 'Hello im ... i need a support to help me with ... . I have '
			body = body.replace(' ', '%20')
			webbrowser.open('mailto:?to=' + recipient + '&subject=' + subject + '&body=' + body, new=1)

		def open_link(self):
			webbrowser.open("https://bugtracker-api.azurewebsites.net/swagger/index.html")

		def report_app(self):
			if self.itemSelectionDetected == True:
				app_id = self.app_list[self.ui.app_list.currentRow()].id
				reportscreen = ReportScreen(user.id,app_id)
				widget.addWidget(reportscreen)
				report_index = 6
				widget.setCurrentIndex(report_index)
			#print(clicked,type(clicked)) Debug 
			#print(self.app_list[clicked].name)

		def clear_app_list(self):
			self.app_list = []
			self.ui.app_list.clear()

		def search_for_app(self):
			
			keyword = self.ui.search_box.text()
			if keyword == '':
				self.reload_app_list()
			else:
				self.clear_app_list()
				link = 'https://bugtracker-api.azurewebsites.net/api/App/SearchByName/'
				r = requests.get(link+keyword)
				for i in r.json():
					self.app_list.append(App(i))
				for a in self.app_list:
					self.ui.app_list.addItem(a.name)
			
		def reload_app_list(self):
			self.clear_app_list()
			self.load_app_list()
			self.itemSelectionDetected = False
			
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
			#print(user.id)
		def trigger_side_menu(self):
			
			if self.side_menu_state == False:
				self.ui.slide_menu_container.setMaximumWidth(250)
			else:
				self.ui.slide_menu_container.setMaximumWidth(0)
			self.side_menu_state = not self.side_menu_state
			
	class ReportScreen(QDialog):
		def __init__(self,user_id,app_id):
			super(ReportScreen, self).__init__()
			self.ui = report_ui.Ui_Dialog()
			self.ui.setupUi(self)
			self.ui.cancel_button.clicked.connect(self.cancel)
			self.ui.report_button.clicked.connect(self.report)
			self.user_id = user_id
			self.app_id = app_id
			print(self.user_id,self.app_id)
		def cancel(self):
			widget.setCurrentIndex(menu_customer_index)
		def report(self):
			#title = self.ui.title_box.text()
			title = self.ui.select_box.currentText()
			desc = self.ui.description_box.toPlainText()
			if title == 'Else' and desc == '':
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Information)

				msg.setText("You need to add description for 'Else' option !!!")
				#msg.setInformativeText("This is additional information")
				msg.setWindowTitle("Caution !!!")
				msg.setWindowIcon(QtGui.QIcon('logo.png'))
				#msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
				msg.setStandardButtons(QMessageBox.Ok)
				retval = msg.exec_()
			else:			
				r = requests.post('https://bugtracker-api.azurewebsites.net/api/Report/Create', json={
				"id": 0,
				"title": title,
				"description": desc,
				"customerId": self.user_id,
				"appId": self.app_id
				})
				#popup report
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Information)

				msg.setText("Thank you for reporting the bug !")
				#msg.setInformativeText("This is additional information")
				msg.setWindowTitle("Thank you !")
				msg.setWindowIcon(QtGui.QIcon('logo.png'))
				#msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
				msg.setStandardButtons(QMessageBox.Ok)
				retval = msg.exec_()
				print("value of pressed message box button:", retval)
				self.ui.description_box.clear()
				self.cancel()

	# run this if main
	if __name__ == "__main__":
		suppress_qt_warnings()

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
		#widget.setCurrentIndex(menu_admin_index)

		mainmenucustomerscreen = MainMenuCustomerScreen()
		widget.addWidget(mainmenucustomerscreen)
		menu_customer_index = 4
		#widget.setCurrentIndex(menu_customer_index)

		mainmenustaffscreen = MainMenuStaffScreen()
		widget.addWidget(mainmenustaffscreen)
		menu_staff_index = 5

		widget.setWindowIcon(QtGui.QIcon('logo.png'))
		widget.setWindowTitle("BugTracker v1")
		widget.setFixedHeight(800)
		widget.setFixedWidth(1200)
		widget.show()
		#loginscreen.show()
		try:
			sys.exit(app.exec())
		except Exception as bug:
			print(bug)
except Exception as bug:
	print(bug)
	input("Enter to close this cmd window!!!")