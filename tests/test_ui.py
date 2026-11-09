import os

from PyQt5 import QtWidgets

from success import success


def test_success_button_closes_window() -> None:
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    window = success()
    window.show()
    window.button_success.click()
    app.processEvents()
    assert not window.isVisible()
