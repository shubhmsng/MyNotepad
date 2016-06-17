from PyQt4.QtGui import *
import sys

class Widget(QWidget):
    def __init__(self, parent=None):
        self.p=""
        self.uname=""
        QWidget.__init__(self, parent)
        self.setGeometry(350, 120, 500, 250)

        self.setWindowIcon(QIcon('favicon.ico'))
        self.setWindowTitle("MyNotepad login")
        frame = QFormLayout()

        self.username = QLineEdit()
        self.user  = QLabel("User Name")
        self.user.setStyleSheet('margin-top:50px; '
                         'color: #66CCFF; '
                         'height:25px;'
                         'font-size: 15px; '
                         'font-family:Arial,Helvetica, sans-serif;'
                         'font-weight:bold'
                         )
        self.username.setStyleSheet('margin-top:50px;'
                       'color: #6495ed;'
                       'height:30px ;'
                       'margin-left: 5px ;'
                       'font-size: 15px; '
                       'font-weight: bold;'
                       'font-family:Arial, Helvetica, sans-serif;'
                       )

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.pas  = QLabel("Password")
        self.pas.setStyleSheet('margin-top:50px; '
                         'color: #66CCFF; '
                         'height:25px;'
                         'font-size: 15px; '
                         'font-family:Arial,Helvetica, sans-serif;'
                         'font-weight:bold'
                         )
        self.password.setStyleSheet('margin-top:50px;'
                       'color: #6495ed;'
                       'height:30px ;'
                       'margin-left: 5px ;'
                       'font-size: 15px; '
                       'font-weight: bold;'
                       'font-family:Arial, Helvetica, sans-serif;'
                       )
        self.btn = QPushButton('Ok', self)
        self.btn.setStyleSheet(
        'height:28px ;'
        'background:#4682B4;'
        'width:30px;'
        'margin-top:30px;'
        'margin-left: 143px ;'
        'margin-right:100px;'
        'font-size: 15px; '
        'color:#ffffff;'
        'font-family:Arial, Helvetica, sans-serif;'
        )
        frame.addRow(self.user,self.username)
        frame.addRow(self.pas,self.password)
        self.btn.clicked.connect(self.onClick)
        frame.addRow(self.btn)

        self.setLayout(frame)


    def onClick(self):
        self.uname = self.username.text()
        self.p = self.password.text()
        if(self.uname=='admin' and self.p =='admin'):
            self.hide()
            import MyNotepad
            self.destroy()
        else:
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Enter correct username and password")
            self.msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())