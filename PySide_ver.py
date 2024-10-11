import sys
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from modules.ui import Ui_MainWindow

class Main(QMainWindow):
    def __init__(self,parent=None):
        super(Main, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # 検索ボタンクリック時
        self.ui.searchBtn.clicked.connect(self.searchForm)
        # エンターキー押下時
        self.ui.nameInput.returnPressed.connect(self.searchForm)
        
    def searchForm(self):
        nameInput = self.ui.nameInput.text()
        if nameInput == "":
            print("無い")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())