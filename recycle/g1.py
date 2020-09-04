# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GreenLabSkive.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
from equipment_package import wind_turbine
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
import GreenLabSkive as gls  

cycle = 0

power_wind = gls.power_wind
power_pv = gls.power_pv

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 740)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1300, 740))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Sche.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.label_co2 = QtWidgets.QLabel(self.centralwidget)
        self.label_co2.setGeometry(QtCore.QRect(200, 670, 60, 13))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_co2.setFont(font)
        self.label_co2.setObjectName("label_co2")

        self.label_wt = QtWidgets.QLabel(self.centralwidget)
        self.label_wt.setGeometry(QtCore.QRect(80, 440, 60, 13))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_wt.setFont(font)
        self.label_wt.setObjectName("label_wt")

        self.label_soc = QtWidgets.QLabel(self.centralwidget)
        self.label_soc.setGeometry(QtCore.QRect(430, 440, 60, 13))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_soc.setFont(font)
        self.label_soc.setObjectName("label_soc")

        self.label_pv = QtWidgets.QLabel(self.centralwidget)
        self.label_pv.setGeometry(QtCore.QRect(80, 240, 60, 13))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_pv.setFont(font)
        self.label_pv.setObjectName("label_pv")

        self.label_biogas = QtWidgets.QLabel(self.centralwidget)
        self.label_biogas.setGeometry(QtCore.QRect(200, 610, 60, 13))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_biogas.setFont(font)
        self.label_biogas.setObjectName("label_biogas")

        self.label_battery = QtWidgets.QLabel(self.centralwidget)
        self.label_battery.setGeometry(QtCore.QRect(280, 370, 60, 13))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_battery.setFont(font)
        self.label_battery.setObjectName("label_battery")

        self.label_elec = QtWidgets.QLabel(self.centralwidget)
        self.label_elec.setGeometry(QtCore.QRect(280, 160, 60, 13))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_elec.setFont(font)
        self.label_elec.setObjectName("label_elec")

        self.label_h2_meth = QtWidgets.QLabel(self.centralwidget)
        self.label_h2_meth.setGeometry(QtCore.QRect(550, 150, 60, 13))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_h2_meth.setFont(font)
        self.label_h2_meth.setObjectName("label_h2_meth")

        self.label_h2_storage = QtWidgets.QLabel(self.centralwidget)
        self.label_h2_storage.setGeometry(QtCore.QRect(810, 670, 60, 13))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_h2_storage.setFont(font)
        self.label_h2_storage.setObjectName("label_h2_storage")

        self.label_h2_s = QtWidgets.QLabel(self.centralwidget)
        self.label_h2_s.setGeometry(QtCore.QRect(550, 250, 41, 16))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_h2_s.setFont(font)
        self.label_h2_s.setObjectName("label_h2_s")

        self.simulate = QtWidgets.QPushButton(self.centralwidget)
        self.simulate.setGeometry(QtCore.QRect(1090, 600, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.simulate.setFont(font)
        self.simulate.setObjectName("simulate")

        self.stop = QtWidgets.QPushButton(self.centralwidget)
        self.stop.setGeometry(QtCore.QRect(1090, 660, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.stop.setFont(font)
        self.stop.setObjectName("stop")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1166, 18))
        self.menubar.setObjectName("menubar")
        self.menuFIle = QtWidgets.QMenu(self.menubar)
        self.menuFIle.setObjectName("menuFIle")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuFIle.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.timer= QTimer()
        self.timer.timeout.connect(self.show)

        self.simulate.clicked.connect(lambda: self.timer.start(1000))
        self.stop.clicked.connect(lambda: self.timer.stop())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_co2.setText(_translate("MainWindow", "CO2:"))
        self.label_wt.setText(_translate("MainWindow", "Power: 0kW"))
        self.label_soc.setText(_translate("MainWindow", "Soc:"))
        self.label_pv.setText(_translate("MainWindow", "Power: 0kW"))
        self.label_biogas.setText(_translate("MainWindow", "Power: 0kW"))
        self.label_battery.setText(_translate("MainWindow", "Power: 0kW"))
        self.label_elec.setText(_translate("MainWindow", "Power: 0kW"))
        self.label_h2_meth.setText(_translate("MainWindow", "H2:"))
        self.label_h2_storage.setText(_translate("MainWindow", "H2:"))
        self.label_h2_s.setText(_translate("MainWindow", "H2:"))
        self.simulate.setText(_translate("MainWindow", "Simulate"))
        self.stop.setText(_translate("MainWindow", "stop"))
        self.menuFIle.setTitle(_translate("MainWindow", "File"))

    def show(self):
        global power_wind, power_pv, cycle
        print(cycle)
        self.label_wt.setText('Power:'+str(round(power_wind[cycle],2))+'kW')
        self.label_wt.adjustSize()
        self.label_pv.setText('Power:'+str(round(power_pv[cycle],2))+'kW')
        self.label_pv.adjustSize()        
        cycle += 1

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
