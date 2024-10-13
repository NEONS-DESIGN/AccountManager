# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'testrFAcxj.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QListView,
    QMainWindow, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(640, 480)
        self.Widget = QWidget(MainWindow)
        self.Widget.setObjectName(u"Widget")
        self.verticalLayoutWidget = QWidget(self.Widget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 620, 460))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.listView = QListView(self.verticalLayoutWidget)
        self.listView.setObjectName(u"listView")

        self.verticalLayout.addWidget(self.listView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.nameInput = QLineEdit(self.verticalLayoutWidget)
        self.nameInput.setObjectName(u"nameInput")

        self.horizontalLayout.addWidget(self.nameInput)

        self.searchBtn = QPushButton(self.verticalLayoutWidget)
        self.searchBtn.setObjectName(u"searchBtn")
        self.searchBtn.setCheckable(False)

        self.horizontalLayout.addWidget(self.searchBtn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.Widget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PasswordManager", None))
        self.nameInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u30a2\u30d7\u30ea\u30fb\u30b5\u30fc\u30d3\u30b9\u540d", None))
        self.searchBtn.setText(QCoreApplication.translate("MainWindow", u"\u691c\u7d22", None))
    # retranslateUi

