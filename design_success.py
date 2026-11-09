from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(250, 100)
        MainWindow.setMinimumSize(QtCore.QSize(250, 100))
        MainWindow.setMaximumSize(QtCore.QSize(250, 100))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button_success = QtWidgets.QPushButton(self.centralwidget)
        self.button_success.setGeometry(QtCore.QRect(50, 25, 150, 50))
        self.button_success.setMinimumSize(QtCore.QSize(150, 50))
        self.button_success.setMaximumSize(QtCore.QSize(150, 50))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiCondensed")
        font.setPointSize(10)
        self.button_success.setFont(font)
        self.button_success.setObjectName("button_success")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Выполнено!"))
        self.button_success.setText(_translate("MainWindow", "Готово"))