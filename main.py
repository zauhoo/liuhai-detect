import sys
import hello
from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = hello.Ui_MainWindow()
    ui.init(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())