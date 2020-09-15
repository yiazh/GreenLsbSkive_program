'''
Created on:

Author: Yi Zheng, Department of Electrical Engineering, DTU

I planned to build a GUI for GreenLabSkive, but I don't think it's the right time to do this. This program basically
indicates the logic of how to build a GUI, although most of its widgets are not well defined and the layout is not o-
gnized.
'''
from PySide2 import QtWidgets
from GUI import main

class my_app(QtWidgets.QMainWindow,main.Ui_MainWindow):
    def __init__(self):
        super(my_app,self).__init__()
        self.setupUi(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication()
    qt_app = my_app()
    qt_app.show()
    app.exec_()