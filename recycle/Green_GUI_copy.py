# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'g2.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
import GreenLabSkive as gls  

cycle = 0

power_wind = gls.power_wind
power_pv = gls.power_pv
electrolyser_out = gls.electrolyser_out


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 800)
        MainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.bg = QtWidgets.QLabel(self.centralwidget)
        self.bg.setGeometry(QtCore.QRect(0, 0, 1500, 800))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap("schematic.png"))
        self.bg.setScaledContents(True)
        self.bg.setObjectName("bg")

        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(1310, 650, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.start.setFont(font)
        self.start.setObjectName("start")

        self.stop = QtWidgets.QPushButton(self.centralwidget)
        self.stop.setGeometry(QtCore.QRect(1310, 700, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        self.stop.setFont(font)
        self.stop.setObjectName("stop")

        self.pv = QtWidgets.QLabel(self.centralwidget)
        self.pv.setGeometry(QtCore.QRect(230, 180, 61, 20))
        self.pv.setObjectName("pv")

        self.wt = QtWidgets.QLabel(self.centralwidget)
        self.wt.setGeometry(QtCore.QRect(230, 400, 61, 20))
        self.wt.setObjectName("wt")

        self.bio_e = QtWidgets.QLabel(self.centralwidget)
        self.bio_e.setGeometry(QtCore.QRect(240, 620, 61, 21))
        self.bio_e.setObjectName("bio_e")

        self.bio_h = QtWidgets.QLabel(self.centralwidget)
        self.bio_h.setGeometry(QtCore.QRect(120, 550, 71, 21))
        self.bio_h.setObjectName("bio_h")

        self.bio_co2 = QtWidgets.QLabel(self.centralwidget)
        self.bio_co2.setGeometry(QtCore.QRect(330, 690, 71, 21))
        self.bio_co2.setObjectName("bio_co2")

        self.co2_buffer_tank = QtWidgets.QLabel(self.centralwidget)
        self.co2_buffer_tank.setGeometry(QtCore.QRect(710, 720, 71, 21))
        self.co2_buffer_tank.setObjectName("co2_buffer_tank")

        self.battery_soc = QtWidgets.QLabel(self.centralwidget)
        self.battery_soc.setGeometry(QtCore.QRect(620, 460, 71, 21))
        self.battery_soc.setObjectName("battery_soc")

        self.h2_buffer = QtWidgets.QLabel(self.centralwidget)
        self.h2_buffer.setGeometry(QtCore.QRect(790, 250, 71, 21))
        self.h2_buffer.setObjectName("h2_buffer")

        self.h2_tank = QtWidgets.QLabel(self.centralwidget)
        self.h2_tank.setGeometry(QtCore.QRect(1210, 730, 71, 21))
        self.h2_tank.setObjectName("h2_tank")

        self.quantafuel_in = QtWidgets.QLabel(self.centralwidget)
        self.quantafuel_in.setGeometry(QtCore.QRect(1100, 360, 71, 21))
        self.quantafuel_in.setObjectName("quantafuel_in")

        self.Metha_co2_in = QtWidgets.QLabel(self.centralwidget)
        self.Metha_co2_in.setGeometry(QtCore.QRect(1100, 220, 81, 21))
        self.Metha_co2_in.setObjectName("Metha_co2_in")

        self.metha_h2_in = QtWidgets.QLabel(self.centralwidget)
        self.metha_h2_in.setGeometry(QtCore.QRect(1100, 160, 35, 10))
        self.metha_h2_in.setObjectName("metha_h2_in")

        self.h2_storage_in = QtWidgets.QLabel(self.centralwidget)
        self.h2_storage_in.setGeometry(QtCore.QRect(1110, 620, 51, 21))
        self.h2_storage_in.setObjectName("h2_storage_in")

        self.elec_in = QtWidgets.QLabel(self.centralwidget)
        self.elec_in.setGeometry(QtCore.QRect(330, 180, 61, 20))
        self.elec_in.setObjectName("elec_in")

        self.elec_out = QtWidgets.QLabel(self.centralwidget)
        self.elec_out.setGeometry(QtCore.QRect(530, 180, 71, 21))
        self.elec_out.setObjectName("elec_out")

        self.meth_electricity_in = QtWidgets.QLabel(self.centralwidget)
        self.meth_electricity_in.setGeometry(QtCore.QRect(1250, 80, 71, 21))
        self.meth_electricity_in.setObjectName("meth_electricity_in")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 18))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.timer= QTimer()
        self.timer.timeout.connect(self.show)

        self.start.clicked.connect(lambda: self.timer.start(1000))
        self.stop.clicked.connect(lambda: self.timer.stop())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start.setText(_translate("MainWindow", "Simulate"))
        self.stop.setText(_translate("MainWindow", "Stop"))
        self.pv.setText(_translate("MainWindow", "kW"))
        self.wt.setText(_translate("MainWindow", "kW"))
        self.bio_e.setText(_translate("MainWindow", "kW"))
        self.bio_h.setText(_translate("MainWindow", "kW"))
        self.bio_co2.setText(_translate("MainWindow", "m3/h"))
        self.co2_buffer_tank.setText(_translate("MainWindow", "m3"))
        self.battery_soc.setText(_translate("MainWindow", "SOC"))
        self.h2_buffer.setText(_translate("MainWindow", "m3"))
        self.h2_tank.setText(_translate("MainWindow", "m3"))
        self.quantafuel_in.setText(_translate("MainWindow", "m3/h"))
        self.Metha_co2_in.setText(_translate("MainWindow", "m3/h"))
        self.metha_h2_in.setText(_translate("MainWindow", "m3/h"))
        self.h2_storage_in.setText(_translate("MainWindow", "m3/h"))
        self.elec_in.setText(_translate("MainWindow", "kW"))
        self.elec_out.setText(_translate("MainWindow", "m3/h"))
        self.meth_electricity_in.setText(_translate("MainWindow", "kW"))

    def show(self):
        global power_wind, power_pv, cycle, electrolyser_out
        print(cycle)
        self.wt.setText(str(round(power_wind[cycle],2))+'kW')
        self.wt.adjustSize()
        self.pv.setText(str(round(power_pv[cycle],2))+'kW')
        self.pv.adjustSize()
        self.elec_in.setText(str(round(power_pv[cycle]+power_wind[cycle],2))+'kW')
        self.elec_in.adjustSize()
        self.elec_out.setText(str(round(gls.electrolyser_out[cycle],2))+'m3/h')
        self.elec_out.adjustSize()     
        self.h2_tank.setText(str(gls.list_add(electrolyser_out,cycle))+'m3')
        self.h2_tank.adjustSize()     
        cycle += 1

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
