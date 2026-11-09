import argparse
import os
import subprocess
import sys
from pathlib import Path

from PyQt5 import QtCore, QtWidgets

import design
from about import about
from collector import collect_logs
from success import success


def stop_usd() -> None:
    result = subprocess.run(
        ["tasklist", "/FI", "IMAGENAME eq UnifiedServiceDesk.exe", "/FO", "CSV", "/NH"],
        capture_output=True,
        check=True,
        timeout=10,
    )
    if b'"UnifiedServiceDesk.exe"' in result.stdout:
        subprocess.run(
            ["taskkill", "/F", "/T", "/IM", "UnifiedServiceDesk.exe"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
            timeout=10,
        )


class Application(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self, source: Path, destination: Path) -> None:
        super().__init__()
        self.setupUi(self)
        self.source = source
        self.destination = destination
        self.success_window = success()
        self.about_window = about()
        self.button_save.clicked.connect(self.click)
        self.about.triggered.connect(self.about_window.show)
        self.text_ldap.textChanged.connect(self.textCheck)

    def click(self) -> None:
        self.button_save.setEnabled(False)
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        try:
            collect_logs(self.source, self.destination, self.text_ldap.text(), stop_usd)
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            QtWidgets.QMessageBox.warning(self, "Не удалось сохранить логи", str(error))
        else:
            self.success_window.show()
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()
            self.textCheck()

    def textCheck(self) -> None:
        value = self.text_ldap.text()
        self.button_save.setEnabled(
            len(value) == 8 and value.isascii() and value.isdigit()
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Сбор логов Unified Service Desk")
    parser.add_argument("--source", type=Path, help="Папка логов USD")
    parser.add_argument(
        "--destination", type=Path, required=True, help="Папка для ZIP-архива"
    )
    args = parser.parse_args()
    if sys.platform != "win32":
        parser.error("Программа сбора логов предназначена для Windows")
    source = args.source
    if source is None:
        appdata = os.environ.get("APPDATA")
        if not appdata:
            parser.error("APPDATA не задана. Укажите папку логов через --source")
        source = (
            Path(appdata)
            / "Microsoft"
            / "Microsoft Dynamics® 365 Unified Service Desk"
            / "4.1.1.1319"
        )
    app = QtWidgets.QApplication([sys.argv[0]])
    window = Application(source, args.destination)
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
