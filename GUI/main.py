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
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frame_18 = QFrame(self.frame)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_18)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_32 = QLabel(self.frame_18)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setPixmap(QPixmap(u":/icons/Modified/New Project.jpg"))

        self.gridLayout_2.addWidget(self.label_32, 0, 0, 2, 2)

        self.label_33 = QLabel(self.frame_18)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setPixmap(QPixmap(u":/icons/Modified/New Project (1).jpg"))
        self.label_33.setScaledContents(True)

        self.gridLayout_2.addWidget(self.label_33, 1, 1, 1, 1)


        self.gridLayout_4.addWidget(self.frame_18, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(652, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 1, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 56, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.frame_25 = QFrame(self.frame)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setMinimumSize(QSize(600, 0))
        self.frame_25.setFrameShape(QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QFrame.Raised)
        self.frame_26 = QFrame(self.frame_25)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setGeometry(QRect(0, 20, 1141, 511))
        self.frame_26.setFrameShape(QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QFrame.Raised)
        self.label_7 = QLabel(self.frame_26)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 10, 571, 351))
        self.label_7.setPixmap(QPixmap(u"Resources/Modified/system.jpg"))
        self.label_7.setScaledContents(True)
        self.frame_29 = QFrame(self.frame_26)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setGeometry(QRect(10, 380, 277, 109))
        self.frame_29.setFrameShape(QFrame.StyledPanel)
        self.frame_29.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_29)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame_28 = QFrame(self.frame_29)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setFrameShape(QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_28)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_8 = QLabel(self.frame_28)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_18.addWidget(self.label_8)

        self.comboBox = QComboBox(self.frame_28)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_18.addWidget(self.comboBox)


        self.verticalLayout_5.addWidget(self.frame_28)

        self.frame_27 = QFrame(self.frame_29)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setFrameShape(QFrame.StyledPanel)
        self.frame_27.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_27)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.pushButton = QPushButton(self.frame_27)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_19.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.frame_27)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_19.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.frame_27)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_19.addWidget(self.pushButton_3)


        self.verticalLayout_5.addWidget(self.frame_27)


        self.gridLayout_4.addWidget(self.frame_25, 2, 0, 1, 2)

        self.frame_24 = QFrame(self.frame)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setFrameShape(QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_24)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame_6 = QFrame(self.frame_24)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(203, 0))
        font = QFont()
        font.setPointSize(8)
        self.frame_6.setFont(font)
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_13 = QLabel(self.frame_6)
        self.label_13.setObjectName(u"label_13")
        font1 = QFont()
        font1.setPointSize(13)
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
        self.label_3.setFont(font)
        self.label_3.setWordWrap(True)

        self.horizontalLayout_5.addWidget(self.label_3)

        self.lineEdit_2 = QLineEdit(self.frame_3)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(40, 0))
        self.lineEdit_2.setMaximumSize(QSize(40, 10000))
        font2 = QFont()
        font2.setPointSize(8)
        font2.setItalic(False)
        self.lineEdit_2.setFont(font2)
        self.lineEdit_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.lineEdit_2)

        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

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
        self.label_5.setFont(font)
        self.label_5.setWordWrap(True)

        self.horizontalLayout_4.addWidget(self.label_5)

        self.lineEdit_3 = QLineEdit(self.frame_4)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMinimumSize(QSize(40, 0))
        self.lineEdit_3.setMaximumSize(QSize(40, 10000))
        self.lineEdit_3.setFont(font2)
        self.lineEdit_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.lineEdit_3)

        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

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
        self.label.setFont(font)

        self.horizontalLayout_3.addWidget(self.label)

        self.lineEdit = QLineEdit(self.frame_2)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(40, 0))
        self.lineEdit.setMaximumSize(QSize(40, 10000))
        self.lineEdit.setFont(font2)
        self.lineEdit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.lineEdit)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

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
        self.label_9.setFont(font)
        self.label_9.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.label_9)

        self.lineEdit_5 = QLineEdit(self.frame_5)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setMinimumSize(QSize(40, 0))
        self.lineEdit_5.setMaximumSize(QSize(40, 10000))
        self.lineEdit_5.setFont(font2)
        self.lineEdit_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.lineEdit_5)

        self.label_10 = QLabel(self.frame_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_10)


        self.verticalLayout.addWidget(self.frame_5)

        self.frame_7 = QFrame(self.frame_6)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_7)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_11 = QLabel(self.frame_7)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(110, 0))
        self.label_11.setFont(font)
        self.label_11.setWordWrap(True)

        self.horizontalLayout.addWidget(self.label_11)

        self.lineEdit_6 = QLineEdit(self.frame_7)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setMinimumSize(QSize(40, 0))
        self.lineEdit_6.setMaximumSize(QSize(40, 10000))
        self.lineEdit_6.setFont(font2)
        self.lineEdit_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.lineEdit_6)

        self.label_12 = QLabel(self.frame_7)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.horizontalLayout.addWidget(self.label_12)


        self.verticalLayout.addWidget(self.frame_7)


        self.gridLayout_3.addWidget(self.frame_6, 0, 2, 2, 1)

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
        font3 = QFont()
        font3.setItalic(False)
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
        self.horizontalLayout_16 = QHBoxLayout(self.frame_22)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_38 = QLabel(self.frame_22)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setMinimumSize(QSize(110, 0))
        self.label_38.setMaximumSize(QSize(105, 16777215))
        self.label_38.setWordWrap(True)

        self.horizontalLayout_16.addWidget(self.label_38)

        self.lineEdit_17 = QLineEdit(self.frame_22)
        self.lineEdit_17.setObjectName(u"lineEdit_17")
        self.lineEdit_17.setMinimumSize(QSize(40, 0))
        self.lineEdit_17.setMaximumSize(QSize(40, 10000))
        self.lineEdit_17.setFont(font3)
        self.lineEdit_17.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_16.addWidget(self.lineEdit_17)

        self.label_39 = QLabel(self.frame_22)
        self.label_39.setObjectName(u"label_39")

        self.horizontalLayout_16.addWidget(self.label_39)


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


        self.gridLayout_3.addWidget(self.frame_19, 2, 1, 1, 2)

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
        self.horizontalLayout_13 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_29 = QLabel(self.frame_17)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setMinimumSize(QSize(110, 0))
        self.label_29.setWordWrap(True)

        self.horizontalLayout_13.addWidget(self.label_29)

        self.lineEdit_14 = QLineEdit(self.frame_17)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        self.lineEdit_14.setMinimumSize(QSize(40, 0))
        self.lineEdit_14.setMaximumSize(QSize(40, 10000))
        self.lineEdit_14.setFont(font3)
        self.lineEdit_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_13.addWidget(self.lineEdit_14)

        self.label_30 = QLabel(self.frame_17)
        self.label_30.setObjectName(u"label_30")

        self.horizontalLayout_13.addWidget(self.label_30)


        self.verticalLayout_4.addWidget(self.frame_17)


        self.gridLayout_3.addWidget(self.frame_13, 1, 0, 2, 1)

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


        self.gridLayout_3.addWidget(self.frame_8, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_24, 2, 2, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_32.setText("")
        self.label_33.setText("")
        self.label_7.setText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Operation strategy", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Wind turbine", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Wind turbine cut-in speed", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"MW", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Wind turbine cut-out speed", None))
        self.lineEdit_3.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"m/s", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Wind turbine capacity", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"MW", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Wind turbine height", None))
        self.lineEdit_5.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"m", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Wind turbine capacity factor", None))
        self.lineEdit_6.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"m", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"Battery", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Serial", None))
        self.lineEdit_15.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_35.setText("")
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Parallel", None))
        self.lineEdit_16.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_37.setText("")
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Capacity", None))
        self.lineEdit_17.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"MW", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Beta", None))
        self.lineEdit_18.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"m", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Electrolyser", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Serial", None))
        self.lineEdit_11.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_23.setText("")
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Paralle", None))
        self.lineEdit_12.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_26.setText("")
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Normal operation cell temperature", None))
        self.lineEdit_13.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"\u2103", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Beta", None))
        self.lineEdit_14.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_30.setText("")
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"PV Panels", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Area", None))
        self.lineEdit_7.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"m2", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Rated module efficiency", None))
        self.lineEdit_8.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_17.setText("")
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Normal operation cell temperature", None))
        self.lineEdit_9.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"\u2103", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Beta", None))
        self.lineEdit_10.setText(QCoreApplication.translate("MainWindow", u"136", None))
        self.label_21.setText("")
    # retranslateUi

