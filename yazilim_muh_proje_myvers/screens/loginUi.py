from PyQt5 import QtCore, QtGui, QtWidgets

class LoginUi(object):
        def setupUi(self, Form):
                Form.setObjectName("ÇalışanGirişi")
                Form.resize(1100, 700)
                Form.setMinimumSize(900, 650)
                Form.setWindowTitle("Kurumsal Yönetim Sistemi")
                
                # ana layout
                self.mainLayout = QtWidgets.QVBoxLayout(Form)
                self.mainLayout.setContentsMargins(30, 30, 30, 30)
                self.mainLayout.setSpacing(0)
                
                # ana container widget
                self.containerWidget = QtWidgets.QWidget()
                self.containerWidget.setObjectName("containerWidget")
                self.containerWidget.setStyleSheet("background-color: #FFFFFF;\n"
                                        "border-radius: 15px;\n")
                
                # container için gölge efekti
                shadow = QtWidgets.QGraphicsDropShadowEffect()
                shadow.setBlurRadius(20)
                shadow.setColor(QtGui.QColor(0, 0, 0, 60))
                shadow.setOffset(0, 5)
                self.containerWidget.setGraphicsEffect(shadow)
                
                # Container layout
                self.containerLayout = QtWidgets.QHBoxLayout(self.containerWidget)
                self.containerLayout.setContentsMargins(0, 0, 0, 0)
                self.containerLayout.setSpacing(0)
                
                # Sol panel - Görsel panel
                self.leftPanel = QtWidgets.QWidget()
                self.leftPanel.setObjectName("leftPanel")
                self.leftPanel.setStyleSheet("background-color: #080121;\n"
                                        "border-top-left-radius: 15px;\n"
                                        "border-bottom-left-radius: 15px;\n")
                
                # Sol panel layout
                self.leftLayout = QtWidgets.QVBoxLayout(self.leftPanel)
                self.leftLayout.setContentsMargins(0, 0, 0, 0)
                self.leftLayout.setSpacing(0)
                
                # logo ekleyeceğimiz alan
                self.logoContainer = QtWidgets.QWidget()
                self.logoContainer.setStyleSheet("background-color: rgba(255, 255, 255, 0.1);\n"
                                        "border-radius: 0px;\n")
                self.logoLayout = QtWidgets.QVBoxLayout(self.logoContainer)
                self.logoLayout.setAlignment(QtCore.Qt.AlignCenter)
                
                # Logo etiketi
                self.logoLabel = QtWidgets.QLabel()
                self.logoLabel.setText("StarTech")
                self.logoLabel.setStyleSheet("font-family: 'Segoe UI', sans-serif;\n"
                                        "font-size: 32px;\n"
                                        "font-weight: bold;\n"
                                        "color: white;\n"
                                        "padding: 20px;\n")
                self.logoLayout.addWidget(self.logoLabel, alignment=QtCore.Qt.AlignCenter)
                
                # Slogan etiketi
                self.sloganLabel = QtWidgets.QLabel()
                self.sloganLabel.setText("KURUMSAL YÖNETİM SİSTEMİ")
                self.sloganLabel.setStyleSheet("font-family: 'Segoe UI', sans-serif;\n"
                                        "font-size: 12px;\n"
                                        "font-weight: 500;\n"
                                        "color: rgba(255, 255, 255, 0.7);\n"
                                        "padding-bottom: 30px;\n")
                self.logoLayout.addWidget(self.sloganLabel, alignment=QtCore.Qt.AlignCenter)
                self.leftLayout.addWidget(self.logoContainer, stretch=3)
                
                # Ana görsel içerik
                self.visualContent = QtWidgets.QWidget()
                self.visualLayout = QtWidgets.QVBoxLayout(self.visualContent)
                self.visualLayout.setContentsMargins(30, 30, 30, 40)
                self.visualLayout.setAlignment(QtCore.Qt.AlignCenter)
                
                # İllüstrasyon
                self.illustrationLabel = QtWidgets.QLabel()
                self.illustrationLabel.setMinimumSize(200, 200)
                self.illustrationLabel.setMaximumSize(300, 300)
                
                pixmap = QtGui.QPixmap('images/hand.png')
                if not pixmap.isNull():
                        self.illustrationLabel.setPixmap(pixmap)
                        self.illustrationLabel.setScaledContents(True)

                self.visualLayout.addWidget(self.illustrationLabel, alignment=QtCore.Qt.AlignCenter)        
                self.leftLayout.addWidget(self.visualContent, stretch=7)
                
                # Sağ panel - Giriş Formu
                self.rightPanel = QtWidgets.QWidget()
                self.rightPanel.setObjectName("rightPanel")
                self.rightPanel.setStyleSheet("background-color: white;\n"
                                "border-top-right-radius: 15px;\n"
                                "border-bottom-right-radius: 15px;\n")
                
                # Sağ panel layout
                self.rightLayout = QtWidgets.QVBoxLayout(self.rightPanel)
                self.rightLayout.setContentsMargins(50, 50, 50, 50)
                self.rightLayout.setSpacing(20)
                self.rightLayout.setAlignment(QtCore.Qt.AlignCenter)
                
                # hoşgeldiniz metni
                self.welcomeLabel = QtWidgets.QLabel()
                self.welcomeLabel.setText("Hoş Geldiniz")
                self.welcomeLabel.setStyleSheet("font-family: 'Segoe UI', sans-serif;\n"
                                        "font-size: 36px;\n"
                                        "font-weight: bold;\n"
                                        "color: #080121;\n")
                self.rightLayout.addWidget(self.welcomeLabel, alignment=QtCore.Qt.AlignCenter)
                
                # alt başlık
                self.subtitleLabel = QtWidgets.QLabel()
                self.subtitleLabel.setText("Kurumsal hesabınızla giriş yapınız")
                self.subtitleLabel.setStyleSheet("font-family: 'Segoe UI', sans-serif;\n"
                                        "font-size: 14px;\n"
                                        "color: #64748B;\n"
                                        "margin-bottom: 30px;\n")
                self.rightLayout.addWidget(self.subtitleLabel, alignment=QtCore.Qt.AlignCenter)
                
                # Giriş formu
                self.formWidget = QtWidgets.QWidget()
                self.formLayout = QtWidgets.QVBoxLayout(self.formWidget)
                self.formLayout.setContentsMargins(0, 0, 0, 0)
                self.formLayout.setSpacing(20)
                
                # Kullanıcı ID Alanı
                self.userMailWidget = QtWidgets.QWidget()
                self.userMailLayout = QtWidgets.QVBoxLayout(self.userMailWidget)
                self.userMailLayout.setContentsMargins(0, 0, 0, 0)
                self.userMailLayout.setSpacing(8)
                
                self.userMailLabel = QtWidgets.QLabel()
                self.userMailLabel.setText("Kurumsal Mail Adresi")
                self.userMailLabel.setStyleSheet("font-family: 'Segoe UI', sans-serif;\n"
                                        "font-size: 13px;\n"
                                        "font-weight: 500;\n"
                                        "color: #64748B;\n")
                self.userMailLayout.addWidget(self.userMailLabel)
                
                self.userMailText = QtWidgets.QLineEdit()
                self.userMailText.setPlaceholderText("Kayıtlı mail adresinizi giriniz")
                self.userMailText.setMinimumHeight(50)
                self.userMailText.setMaximumHeight(50)
                self.userMailText.setStyleSheet("font-family: 'Segoe UI', sans-serif;\n"
                                        "font-size: 14px;\n"
                                        "color: #080121;\n"
                                        "background-color: #F1F5F9;\n"
                                        "border: 1px solid #E2E8F0;\n"
                                        "border-radius: 8px;\n"
                                        "padding: 0 15px;\n")
                self.userMailLayout.addWidget(self.userMailText)
                
                self.formLayout.addWidget(self.userMailWidget)
                
                # Şifre Alanı
                self.passwordWidget = QtWidgets.QWidget()
                self.passwordLayout = QtWidgets.QVBoxLayout(self.passwordWidget)
                self.passwordLayout.setContentsMargins(0, 0, 0, 0)
                self.passwordLayout.setSpacing(8)
                
                self.passwordLabel = QtWidgets.QLabel()
                self.passwordLabel.setText("Şifre")
                self.passwordLabel.setStyleSheet("font-family: 'Segoe UI', sans-serif;\n"
                                        "font-size: 13px;\n"
                                        "font-weight: 500;\n"
                                        "color: #64748B;\n")
                self.passwordLayout.addWidget(self.passwordLabel)
                
                self.passwordText = QtWidgets.QLineEdit()
                self.passwordText.setPlaceholderText("Şifrenizi girin")
                self.passwordText.setEchoMode(QtWidgets.QLineEdit.Password)
                self.passwordText.setMinimumHeight(50)
                self.passwordText.setMaximumHeight(50)
                self.passwordText.setStyleSheet("font-family: 'Segoe UI', sans-serif;\n"
                                        "font-size: 14px;\n"
                                        "color: #080121;\n"
                                        "background-color: #F1F5F9;\n"
                                        "border: 1px solid #E2E8F0;\n"
                                        "border-radius: 8px;\n"
                                        "padding: 0 15px;\n")
                self.passwordLayout.addWidget(self.passwordText)
                
                self.formLayout.addWidget(self.passwordWidget)
                
                # Hatırla ve Şifremi Unuttum satırı
                self.optionsWidget = QtWidgets.QWidget()
                self.optionsLayout = QtWidgets.QHBoxLayout(self.optionsWidget)
                self.optionsLayout.setContentsMargins(0, 0, 0, 0)
                self.optionsLayout.setSpacing(0)
                
                self.rememberMe = QtWidgets.QCheckBox()
                self.rememberMe.setText("Beni hatırla")
                self.rememberMe.setStyleSheet("font-family: 'Segoe UI', sans-serif;\n"
                                        "font-size: 13px;\n"
                                        "color: #64748B;\n")
                self.optionsLayout.addWidget(self.rememberMe)
                
                self.optionsLayout.addStretch()
                
                # Giriş butonu
                self.loginButton = QtWidgets.QPushButton()
                self.loginButton.setText("GİRİŞ YAP")
                self.loginButton.setMinimumHeight(50)
                self.loginButton.setMaximumHeight(50)
                self.loginButton.setStyleSheet("font-family: 'Segoe UI', sans-serif;\n"
                                        "font-size: 14px;\n"
                                        "font-weight: bold;\n"
                                        "color: white;\n"
                                        "background-color: #080121;\n"
                                        "border-radius: 8px;\n"
                                        "border: none;\n")
                # Buton için gölge efekti
                button_shadow = QtWidgets.QGraphicsDropShadowEffect()
                button_shadow.setBlurRadius(15)
                button_shadow.setColor(QtGui.QColor(30, 58, 138, 60))
                button_shadow.setOffset(0, 5)
                self.loginButton.setGraphicsEffect(button_shadow)
                
                self.formLayout.addWidget(self.loginButton)
                
                # Form widget'ını sağ panele ekleme
                self.rightLayout.addWidget(self.formWidget)
                
                # Container'a panelleri ekleme
                self.containerLayout.addWidget(self.leftPanel, 5)  # %50 oranında genişlik
                self.containerLayout.addWidget(self.rightPanel, 5)
                
                # Ana container'ı layout'a ekleme
                self.mainLayout.addWidget(self.containerWidget)
                
                # Pencere yeniden boyutlandırıldığında olay
                Form.resizeEvent = self.on_resize_event

        def on_resize_event(self, event):
                QtWidgets.QWidget.resizeEvent(self.containerWidget, event) #pencerenin yeniden boyutlandırılması işlemi
