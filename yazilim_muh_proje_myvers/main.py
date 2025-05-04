import PyQt5.QtWidgets as QtWidgets
import sys
from screens.loginUi import LoginUi
from screens.dashboard import DashboardUI
from models.database import Database

class giderApp(QtWidgets.QWidget, LoginUi):
    def __init__(self):
        super(giderApp, self).__init__()
        self.setupUi(self)
        self.db = Database()  # veritabanı nesnesi
        self.userMailText.returnPressed.connect(self.on_login_click)
        self.passwordText.returnPressed.connect(self.on_login_click)
        self.loginButton.clicked.connect(self.on_login_click)

    def on_login_click(self):
        email = self.userMailText.text()
        password = self.passwordText.text()

        user = self.db.authUser(email, password)

        if user:
            if user["user_type"] == "ustyonetici":
                self.open_dashboard(user) #bu üst yönetim için kullanılan bir metod
            elif user["user_type"] == "yonetici":
                QtWidgets.QMessageBox.information(self, "Bilgi", "Yönetici paneli henüz hazır değil.")
            elif user["user_type"] == "calisan":
                QtWidgets.QMessageBox.information(self, "Bilgi", "Çalışan paneli henüz hazır değil.")
            elif user["user_type"] == "muhasebe":
                QtWidgets.QMessageBox.information(self, "Bilgi", "Muhasebe paneli henüz hazır değil.")
        else:
            QtWidgets.QMessageBox.warning(self, "Hatalı Giriş", "E-posta veya şifre hatalı!")

    def open_dashboard(self, user=None):
        from screens.dashboard import DashboardUI
        self.dashboard_window = QtWidgets.QWidget()
        self.dashboard_ui = DashboardUI()
        self.dashboard_ui.setupUi(self.dashboard_window)
        self.dashboard_ui.btn_home.clicked.connect(self.reopen_dashboard)
        self.dashboard_window.show()
        self.hide()

    def reopen_dashboard(self):
        self.dashboard_window.show()
        self.hide()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = giderApp()
    Form.show()
    sys.exit(app.exec_())