import sys

from PyQt5 import QtWidgets

from design_about import Ui_MainWindow


class about(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = about()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
