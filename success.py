import sys

from PyQt5 import QtWidgets

from design_success import Ui_MainWindow


class success(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.button_success.clicked.connect(self.close)


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = success()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
