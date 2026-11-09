from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(350, 250)
        MainWindow.setMinimumSize(QtCore.QSize(350, 250))
        MainWindow.setMaximumSize(QtCore.QSize(350, 250))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_about = QtWidgets.QLabel(self.centralwidget)
        self.label_about.setGeometry(QtCore.QRect(70, 20, 210, 200))
        self.label_about.setMinimumSize(QtCore.QSize(210, 200))
        self.label_about.setMaximumSize(QtCore.QSize(210, 200))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiCondensed")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_about.setFont(font)
        self.label_about.setObjectName("label_about")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "О программе"))
        self.label_about.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Сбор логов Microsoft Dynamics 365 Unified Service Desk</p><p align=\"center\">Архивная Windows-утилита</p><p align=\"center\">ver. 0.1</p></body></html>"))
