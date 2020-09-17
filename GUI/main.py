# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import Icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 817)
        MainWindow.setMinimumSize(QSize(1200, 817))
        MainWindow.setMaximumSize(QSize(1200, 817))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame_25 = QFrame(self.frame)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setGeometry(QRect(20, 120, 600, 621))
        self.frame_25.setMinimumSize(QSize(600, 0))
        self.frame_25.setFrameShape(QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QFrame.Raised)
        self.frame_26 = QFrame(self.frame_25)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setGeometry(QRect(0, 0, 591, 511))
        self.frame_26.setFrameShape(QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QFrame.Raised)
        self.label_7 = QLabel(self.frame_26)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 10, 571, 351))
        self.label_7.setMaximumSize(QSize(571, 351))
        self.label_7.setPixmap(QPixmap(u"Resources/Modified/system.jpg"))
        self.label_7.setScaledContents(True)
        self.frame_29 = QFrame(self.frame_26)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setGeometry(QRect(10, 380, 311, 121))
        self.frame_29.setFrameShape(QFrame.StyledPanel)
        self.frame_29.setFrameShadow(QFrame.Raised)
        self.frame_28 = QFrame(self.frame_29)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setGeometry(QRect(10, 10, 291, 40))
        self.frame_28.setFrameShape(QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_28)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_8 = QLabel(self.frame_28)
        self.label_8.setObjectName(u"label_8")
        font = QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)

        self.horizontalLayout_19.addWidget(self.label_8)

        self.comboBox = QComboBox(self.frame_28)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(111, 0))

        self.horizontalLayout_19.addWidget(self.comboBox)

        self.frame_27 = QFrame(self.frame_29)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setGeometry(QRect(10, 64, 261, 43))
        self.frame_27.setFrameShape(QFrame.StyledPanel)
        self.frame_27.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_27)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.pushButton = QPushButton(self.frame_27)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_18.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.frame_27)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_18.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.frame_27)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_18.addWidget(self.pushButton_3)

        self.frame_30 = QFrame(self.frame_26)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setGeometry(QRect(330, 380, 241, 118))
        self.frame_30.setFrameShape(QFrame.StyledPanel)
        self.frame_30.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_30)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_44 = QLabel(self.frame_30)
        self.label_44.setObjectName(u"label_44")
        font1 = QFont()
        font1.setPointSize(13)
        self.label_44.setFont(font1)

        self.verticalLayout_5.addWidget(self.label_44)

        self.textBrowser = QTextBrowser(self.frame_30)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setMaximumSize(QSize(191, 71))

        self.verticalLayout_5.addWidget(self.textBrowser)

        self.frame_24 = QFrame(self.frame)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setGeometry(QRect(640, 119, 462, 570))
        self.frame_24.setFrameShape(QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_24)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_43 = QLabel(self.frame_24)
        self.label_43.setObjectName(u"label_43")
        font2 = QFont()
        font2.setPointSize(15)
        self.label_43.setFont(font2)

        self.gridLayout_2.addWidget(self.label_43, 0, 0, 1, 1)

        self.frame_8 = QFrame(self.frame_24)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(209, 0))
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_24 = QLabel(self.frame_8)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font1)
        self.label_24.setTextFormat(Qt.AutoText)

        self.verticalLayout_2.addWidget(self.label_24)

        self.frame_9 = QFrame(self.frame_8)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(0, 20))
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_14 = QLabel(self.frame_9)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(110, 0))
        self.label_14.setWordWrap(True)

        self.horizontalLayout_6.addWidget(self.label_14)

        self.lineEdit_7 = QLineEdit(self.frame_9)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setMinimumSize(QSize(40, 0))
        self.lineEdit_7.setMaximumSize(QSize(40, 10000))
        font3 = QFont()
        font3.setItalic(False)
        self.lineEdit_7.setFont(font3)
        self.lineEdit_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.lineEdit_7)

        self.label_15 = QLabel(self.frame_9)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_6.addWidget(self.label_15)


        self.verticalLayout_2.addWidget(self.frame_9)

        self.frame_10 = QFrame(self.frame_8)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_16 = QLabel(self.frame_10)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(110, 0))
        self.label_16.setWordWrap(True)

        self.horizontalLayout_7.addWidget(self.label_16)

        self.lineEdit_8 = QLineEdit(self.frame_10)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setMinimumSize(QSize(40, 0))
        self.lineEdit_8.setMaximumSize(QSize(40, 10000))
        self.lineEdit_8.setFont(font3)
        self.lineEdit_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.lineEdit_8)

        self.label_17 = QLabel(self.frame_10)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_7.addWidget(self.label_17)


        self.verticalLayout_2.addWidget(self.frame_10)

        self.frame_11 = QFrame(self.frame_8)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_18 = QLabel(self.frame_11)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(110, 0))
        self.label_18.setMaximumSize(QSize(105, 16777215))
        self.label_18.setWordWrap(True)

        self.horizontalLayout_8.addWidget(self.label_18)

        self.lineEdit_9 = QLineEdit(self.frame_11)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setMinimumSize(QSize(40, 0))
        self.lineEdit_9.setMaximumSize(QSize(40, 10000))
        self.lineEdit_9.setFont(font3)
        self.lineEdit_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.lineEdit_9)

        self.label_19 = QLabel(self.frame_11)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_8.addWidget(self.label_19)


        self.verticalLayout_2.addWidget(self.frame_11)

        self.frame_12 = QFrame(self.frame_8)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_20 = QLabel(self.frame_12)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(110, 0))
        self.label_20.setWordWrap(True)

        self.horizontalLayout_9.addWidget(self.label_20)

        self.lineEdit_10 = QLineEdit(self.frame_12)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setMinimumSize(QSize(40, 0))
        self.lineEdit_10.setMaximumSize(QSize(40, 10000))
        self.lineEdit_10.setFont(font3)
        self.lineEdit_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.lineEdit_10)

        self.label_21 = QLabel(self.frame_12)
        self.label_21.setObjectName(u"label_21")

        self.horizontalLayout_9.addWidget(self.label_21)


        self.verticalLayout_2.addWidget(self.frame_12)


        self.gridLayout_2.addWidget(self.frame_8, 1, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_24)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(203, 0))
        font4 = QFont()
        font4.setPointSize(8)
        self.frame_6.setFont(font4)
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_13 = QLabel(self.frame_6)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font1)
        self.label_13.setTextFormat(Qt.AutoText)

        self.verticalLayout.addWidget(self.label_13)

        self.frame_3 = QFrame(self.frame_6)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 20))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(110, 0))
        self.label_3.setFont(font4)
        self.label_3.setWordWrap(True)

        self.horizontalLayout_5.addWidget(self.label_3)

        self.lineEdit_2 = QLineEdit(self.frame_3)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(40, 0))
        self.lineEdit_2.setMaximumSize(QSize(40, 10000))
        font5 = QFont()
        font5.setPointSize(8)
        font5.setItalic(False)
        self.lineEdit_2.setFont(font5)
        self.lineEdit_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.lineEdit_2)

        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font4)

        self.horizontalLayout_5.addWidget(self.label_4)


        self.verticalLayout.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame_6)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(110, 0))
        self.label_5.setFont(font4)
        self.label_5.setWordWrap(True)

        self.horizontalLayout_4.addWidget(self.label_5)

        self.lineEdit_3 = QLineEdit(self.frame_4)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMinimumSize(QSize(40, 0))
        self.lineEdit_3.setMaximumSize(QSize(40, 10000))
        self.lineEdit_3.setFont(font5)
        self.lineEdit_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.lineEdit_3)

        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font4)

        self.horizontalLayout_4.addWidget(self.label_6)


        self.verticalLayout.addWidget(self.frame_4)

        self.frame_2 = QFrame(self.frame_6)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(110, 0))
        self.label.setMaximumSize(QSize(105, 16777215))
        self.label.setFont(font4)

        self.horizontalLayout_3.addWidget(self.label)

        self.lineEdit = QLineEdit(self.frame_2)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(40, 0))
        self.lineEdit.setMaximumSize(QSize(40, 10000))
        self.lineEdit.setFont(font5)
        self.lineEdit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.lineEdit)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font4)

        self.horizontalLayout_3.addWidget(self.label_2)


        self.verticalLayout.addWidget(self.frame_2)

        self.frame_5 = QFrame(self.frame_6)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_9 = QLabel(self.frame_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(110, 0))
        self.label_9.setFont(font4)
        self.label_9.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.label_9)

        self.lineEdit_5 = QLineEdit(self.frame_5)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setMinimumSize(QSize(40, 0))
        self.lineEdit_5.setMaximumSize(QSize(40, 10000))
        self.lineEdit_5.setFont(font5)
        self.lineEdit_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.lineEdit_5)

        self.label_10 = QLabel(self.frame_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font4)

        self.horizontalLayout_2.addWidget(self.label_10)


        self.verticalLayout.addWidget(self.frame_5)

        self.frame_7 = QFrame(self.frame_6)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.label_11 = QLabel(self.frame_7)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(10, 10, 110, 26))
        self.label_11.setMinimumSize(QSize(110, 0))
        self.label_11.setFont(font4)
        self.label_11.setWordWrap(True)
        self.lineEdit_6 = QLineEdit(self.frame_7)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setGeometry(QRect(127, 10, 40, 26))
        self.lineEdit_6.setMinimumSize(QSize(40, 0))
        self.lineEdit_6.setMaximumSize(QSize(40, 10000))
        self.lineEdit_6.setFont(font5)
        self.lineEdit_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.frame_7)


        self.gridLayout_2.addWidget(self.frame_6, 1, 1, 2, 1)

        self.frame_13 = QFrame(self.frame_24)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMinimumSize(QSize(203, 0))
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_13)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_31 = QLabel(self.frame_13)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font1)
        self.label_31.setTextFormat(Qt.AutoText)

        self.verticalLayout_4.addWidget(self.label_31)

        self.frame_14 = QFrame(self.frame_13)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setMinimumSize(QSize(0, 20))
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_22 = QLabel(self.frame_14)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(110, 0))
        self.label_22.setWordWrap(True)

        self.horizontalLayout_10.addWidget(self.label_22)

        self.lineEdit_11 = QLineEdit(self.frame_14)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        self.lineEdit_11.setMinimumSize(QSize(40, 0))
        self.lineEdit_11.setMaximumSize(QSize(40, 10000))
        self.lineEdit_11.setFont(font3)
        self.lineEdit_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_10.addWidget(self.lineEdit_11)

        self.label_23 = QLabel(self.frame_14)
        self.label_23.setObjectName(u"label_23")

        self.horizontalLayout_10.addWidget(self.label_23)


        self.verticalLayout_4.addWidget(self.frame_14)

        self.frame_15 = QFrame(self.frame_13)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_25 = QLabel(self.frame_15)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(110, 0))
        self.label_25.setWordWrap(True)

        self.horizontalLayout_11.addWidget(self.label_25)

        self.lineEdit_12 = QLineEdit(self.frame_15)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        self.lineEdit_12.setMinimumSize(QSize(40, 0))
        self.lineEdit_12.setMaximumSize(QSize(40, 10000))
        self.lineEdit_12.setFont(font3)
        self.lineEdit_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.lineEdit_12)

        self.label_26 = QLabel(self.frame_15)
        self.label_26.setObjectName(u"label_26")

        self.horizontalLayout_11.addWidget(self.label_26)


        self.verticalLayout_4.addWidget(self.frame_15)

        self.frame_16 = QFrame(self.frame_13)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_27 = QLabel(self.frame_16)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMinimumSize(QSize(110, 0))
        self.label_27.setMaximumSize(QSize(105, 16777215))
        self.label_27.setWordWrap(True)

        self.horizontalLayout_12.addWidget(self.label_27)

        self.lineEdit_13 = QLineEdit(self.frame_16)
        self.lineEdit_13.setObjectName(u"lineEdit_13")
        self.lineEdit_13.setMinimumSize(QSize(40, 0))
        self.lineEdit_13.setMaximumSize(QSize(40, 10000))
        self.lineEdit_13.setFont(font3)
        self.lineEdit_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.lineEdit_13)

        self.label_28 = QLabel(self.frame_16)
        self.label_28.setObjectName(u"label_28")

        self.horizontalLayout_12.addWidget(self.label_28)


        self.verticalLayout_4.addWidget(self.frame_16)

        self.frame_17 = QFrame(self.frame_13)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.label_29 = QLabel(self.frame_17)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setGeometry(QRect(10, 10, 110, 26))
        self.label_29.setMinimumSize(QSize(110, 0))
        self.label_29.setWordWrap(True)
        self.lineEdit_14 = QLineEdit(self.frame_17)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        self.lineEdit_14.setGeometry(QRect(125, 10, 40, 27))
        self.lineEdit_14.setMinimumSize(QSize(40, 0))
        self.lineEdit_14.setMaximumSize(QSize(40, 10000))
        self.lineEdit_14.setFont(font3)
        self.lineEdit_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_30 = QLabel(self.frame_17)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setGeometry(QRect(169, 14, 25, 16))

        self.verticalLayout_4.addWidget(self.frame_17)


        self.gridLayout_2.addWidget(self.frame_13, 2, 0, 2, 1)

        self.frame_19 = QFrame(self.frame_24)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setMinimumSize(QSize(209, 0))
        self.frame_19.setFrameShape(QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_19)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_42 = QLabel(self.frame_19)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setFont(font1)
        self.label_42.setTextFormat(Qt.AutoText)

        self.verticalLayout_3.addWidget(self.label_42)

        self.frame_20 = QFrame(self.frame_19)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setMinimumSize(QSize(0, 20))
        self.frame_20.setFrameShape(QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_34 = QLabel(self.frame_20)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setMinimumSize(QSize(110, 0))
        self.label_34.setWordWrap(True)

        self.horizontalLayout_14.addWidget(self.label_34)

        self.lineEdit_15 = QLineEdit(self.frame_20)
        self.lineEdit_15.setObjectName(u"lineEdit_15")
        self.lineEdit_15.setMinimumSize(QSize(40, 0))
        self.lineEdit_15.setMaximumSize(QSize(40, 10000))
        self.lineEdit_15.setFont(font3)
        self.lineEdit_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_14.addWidget(self.lineEdit_15)

        self.label_35 = QLabel(self.frame_20)
        self.label_35.setObjectName(u"label_35")

        self.horizontalLayout_14.addWidget(self.label_35)


        self.verticalLayout_3.addWidget(self.frame_20)

        self.frame_21 = QFrame(self.frame_19)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_21)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_36 = QLabel(self.frame_21)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setMinimumSize(QSize(110, 0))
        self.label_36.setWordWrap(True)

        self.horizontalLayout_15.addWidget(self.label_36)

        self.lineEdit_16 = QLineEdit(self.frame_21)
        self.lineEdit_16.setObjectName(u"lineEdit_16")
        self.lineEdit_16.setMinimumSize(QSize(40, 0))
        self.lineEdit_16.setMaximumSize(QSize(40, 10000))
        self.lineEdit_16.setFont(font3)
        self.lineEdit_16.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_15.addWidget(self.lineEdit_16)

        self.label_37 = QLabel(self.frame_21)
        self.label_37.setObjectName(u"label_37")

        self.horizontalLayout_15.addWidget(self.label_37)


        self.verticalLayout_3.addWidget(self.frame_21)

        self.frame_22 = QFrame(self.frame_19)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setFrameShape(QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Raised)
        self.label_38 = QLabel(self.frame_22)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setGeometry(QRect(10, 10, 110, 16))
        self.label_38.setMinimumSize(QSize(110, 0))
        self.label_38.setMaximumSize(QSize(105, 16777215))
        self.label_38.setWordWrap(True)
        self.lineEdit_17 = QLineEdit(self.frame_22)
        self.lineEdit_17.setObjectName(u"lineEdit_17")
        self.lineEdit_17.setGeometry(QRect(126, 10, 40, 20))
        self.lineEdit_17.setMinimumSize(QSize(40, 0))
        self.lineEdit_17.setMaximumSize(QSize(40, 10000))
        self.lineEdit_17.setFont(font3)
        self.lineEdit_17.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_39 = QLabel(self.frame_22)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setGeometry(QRect(169, 11, 18, 16))

        self.verticalLayout_3.addWidget(self.frame_22)

        self.frame_23 = QFrame(self.frame_19)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setFrameShape(QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_23)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_40 = QLabel(self.frame_23)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setMinimumSize(QSize(110, 0))
        self.label_40.setWordWrap(True)

        self.horizontalLayout_17.addWidget(self.label_40)

        self.lineEdit_18 = QLineEdit(self.frame_23)
        self.lineEdit_18.setObjectName(u"lineEdit_18")
        self.lineEdit_18.setMinimumSize(QSize(40, 0))
        self.lineEdit_18.setMaximumSize(QSize(40, 10000))
        self.lineEdit_18.setFont(font3)
        self.lineEdit_18.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_17.addWidget(self.lineEdit_18)

        self.label_41 = QLabel(self.frame_23)
        self.label_41.setObjectName(u"label_41")

        self.horizontalLayout_17.addWidget(self.label_41)


        self.verticalLayout_3.addWidget(self.frame_23)


        self.gridLayout_2.addWidget(self.frame_19, 3, 1, 1, 1)

        self.frame_18 = QFrame(self.frame)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setGeometry(QRect(20, 10, 251, 91))
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.label_32 = QLabel(self.frame_18)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setGeometry(QRect(10, 10, 16, 16))
        self.label_32.setPixmap(QPixmap(u":/icons/Modified/New Project.jpg"))
        self.label_33 = QLabel(self.frame_18)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setGeometry(QRect(10, 10, 231, 81))
        self.label_33.setPixmap(QPixmap(u":/icons/Modified/New Project (1).jpg"))
        self.label_33.setScaledContents(True)

        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_7.setText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Operation strategy", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Profit maximization", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Cost minimization ", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Efficiency maximization", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"CO2 minimization", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"100% Green Products", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"100% reliable energy supply", None))

        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Calculate", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Sumulate", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Results", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Net present value: *** \u20ac</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Internal rate of return: *** \u20ac</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">CO2 emmission: ***kg</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px"
                        "; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"PV Panels", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Area", None))
        self.lineEdit_7.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"m2", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Rated module efficiency", None))
        self.lineEdit_8.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.label_17.setText("")
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Normal operation cell temperature", None))
        self.lineEdit_9.setText(QCoreApplication.translate("MainWindow", u"25", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"\u2103", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Beta", None))
        self.lineEdit_10.setText(QCoreApplication.translate("MainWindow", u"0.43", None))
        self.label_21.setText("")
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Wind turbine", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Wind turbine cut-in speed", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"m/s", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Wind turbine cut-out speed", None))
        self.lineEdit_3.setText(QCoreApplication.translate("MainWindow", u"25", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"m/s", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Wind turbine capacity", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"13", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"MW", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Wind turbine height", None))
        self.lineEdit_5.setText(QCoreApplication.translate("MainWindow", u"50", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"m", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Wind turbine capacity factor", None))
        self.lineEdit_6.setText(QCoreApplication.translate("MainWindow", u"0.36", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Electrolyser", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Serial", None))
        self.lineEdit_11.setText(QCoreApplication.translate("MainWindow", u"50", None))
        self.label_23.setText("")
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Paralle", None))
        self.lineEdit_12.setText(QCoreApplication.translate("MainWindow", u"60", None))
        self.label_26.setText("")
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Normal operation cell temperature", None))
        self.lineEdit_13.setText(QCoreApplication.translate("MainWindow", u"25", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"\u2103", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Exchange current density", None))
        self.lineEdit_14.setText(QCoreApplication.translate("MainWindow", u"5000", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"A/m2", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"Battery", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Serial", None))
        self.lineEdit_15.setText(QCoreApplication.translate("MainWindow", u"50", None))
        self.label_35.setText("")
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Parallel", None))
        self.lineEdit_16.setText(QCoreApplication.translate("MainWindow", u"60", None))
        self.label_37.setText("")
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Capacity", None))
        self.lineEdit_17.setText(QCoreApplication.translate("MainWindow", u"1.36", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"MW", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Voltage", None))
        self.lineEdit_18.setText(QCoreApplication.translate("MainWindow", u"12", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"V", None))
        self.label_32.setText("")
        self.label_33.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

