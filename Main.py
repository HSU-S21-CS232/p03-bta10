import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QLineEdit, QPushButton

from PySide2.QtCore import QFile, QObject

class MainWindow(QObject):

    def __init__(self, ui_file, parent=None):

        super(MainWindow, self).__init__(parent)

        ui_file = Qfile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)

        ui_file.close()

        self.window.show()

if __name__ == '__Main__':
    app = QApplication(sys.argv)
    main_window = MainWindow('Name.ui')
    sys.exit(app.exec_())
