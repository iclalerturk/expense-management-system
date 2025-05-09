import PyQt5.QtWidgets as QtWidgets
import sys
from screens.loginUi import LoginUi
from screens.dashboard import DashboardUI
from screens.yönetici_panel import YoneticiPanelUI
from screens.employee_dashboard import EmployeeDashboardUI
from screens.muhasebe import MuhasebeDashboardUI  
from models.database import Database

class giderApp(QtWidgets.QWidget, LoginUi):
    def __init__(self):
        super(giderApp, self).__init__()
        self.setupUi(self)
        self.db = Database()  # veritabanı nesnesiz
        self.userMailText.returnPressed.connect(self.on_login_click)
        self.passwordText.returnPressed.connect(self.on_login_click)
        self.loginButton.clicked.connect(self.on_login_click)
        # self.db=Database()  # veritabanı nesnesini oluştur
        # self.db.add_max_kisi_limit()
    def on_login_click(self):
        email = self.userMailText.text()
        password = self.passwordText.text()

        user = self.db.authUser(email, password)

        if user:
            if user["user_type"] == "ustyonetici":
                self.open_dashboard(user) #bu üst yönetim için kullanılan bir metod
            elif user["user_type"] == "yonetici":
                self.open_yonetici_panel(user) # yönetici paneli
            elif user["user_type"] == "calisan":
                self.open_employee_dashboard(user)  # Çalışan panelini aç
            elif user["user_type"] == "muhasebe":
                # QtWidgets.QMessageBox.information(self, "Bilgi", "Muhasebe paneli henüz hazır değil.")
                self.open_muhasebe_panel(user)  # Muhasebe panelini aç
        else:
            QtWidgets.QMessageBox.warning(self, "Hatalı Giriş", "E-posta veya şifre hatalı!")

    def open_muhasebe_panel(self, user=None):
        self.muhasebe_window = QtWidgets.QWidget()
        self.muhasebe_ui = MuhasebeDashboardUI()
        self.muhasebe_ui.setupUi(self.muhasebe_window)
        self.muhasebe_ui.set_user(user)
        
        # Çıkış butonu işlevi
        self.muhasebe_ui.btn_logout.clicked.connect(self.logout_employee)
        
        # Arayüzü göster
        self.muhasebe_window.show()
        self.hide()

    def open_dashboard(self, user=None):
        self.dashboard_window = QtWidgets.QWidget()
        self.dashboard_ui = DashboardUI()
        self.dashboard_ui.setupUi(self.dashboard_window)
        self.dashboard_ui.btn_home.clicked.connect(self.reopen_dashboard)
        self.dashboard_window.show()
        self.hide()

    def open_employee_dashboard(self, user=None):
        self.employee_window = QtWidgets.QWidget()
        self.employee_ui = EmployeeDashboardUI()
        self.employee_ui.setupUi(self.employee_window)
        self.employee_ui.set_user(user)
        
        
        # Çıkış butonu işlevi
        self.employee_ui.btn_logout.clicked.connect(self.logout_employee)
        
        # Arayüzü göster
        self.employee_window.show()
        self.hide()

    def logout_employee(self):
        # Çalışan arayüzünü kapat ve giriş ekranını göster
        if hasattr(self, 'employee_window'):
            self.employee_window.close()
        self.show()

    def reopen_dashboard(self):
        self.dashboard_window.show()
        self.hide()

    def open_yonetici_panel(self, user):
        
        self.yonetici_window = QtWidgets.QMainWindow()
        self.yonetici_ui = YoneticiPanelUI()
        self.yonetici_ui.parent_window = self.yonetici_window  
        self.yonetici_ui.login_window = self  
        self.yonetici_ui.setupUi(self.yonetici_window, user["birimId"])
        self.yonetici_window.show()
        self.hide()

    def show_login_again(self):
        self.show()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = giderApp()
    Form.show()
    sys.exit(app.exec_())
