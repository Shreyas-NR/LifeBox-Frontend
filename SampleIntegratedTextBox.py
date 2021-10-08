from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
import serial
import time
from datetime import datetime

from pyqtgraph import PlotWidget, plot, exporters
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint

import csv
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QThread,QTimer
GUIOBJECT = None  # Global variable for the GUI
Plotting_Thread = None
AverageTemperature = 0  # Global variable for Average Temperature
TopTemperature = 0  # Use global variable TopTemperature
BottomTemperature = 0  # Use global variable BottomTemperature
HeartTemperature = 0  # Use global variable HeartTemperature
DryIce = 0  # Use global variable DryIce
BlowerPWM = 0
TopTemperature_s = 0
TopTemperature_f = 0
BottomTemperature_s = 0
BottomTemperature_f = 0
AverageTemperature_s = 0
AverageTemperature_f = 0
HeartTemperature_s = 0
HeartTemperature_f = 0
DryIceLoad_s = 0
DryIceLoad_f = 0
SalineOneLoad_s = 0
SalineOneLoad_f = 0
SalineTwoLoad_s = 0
SalineTwoLoad_f = 0
BlowerPWM_s = 0
BlowerPWM_f = 0
BlowerPIDOutput_s = 0
BlowerPIDOutput_f = 0
Blower_On_Off_s = 0
Blower_On_Off_f = 0
Exhaust_On_Off_s = 0
Exhaust_On_Off_f = 0
GsecCounter_s = 0
GsecCounter_f = 0
SecondCount_s = 0
SecondCount_f = 0
ReqPerfusionData_s = 0
ReqPerfusionTime_s = 0
PumpOneStatus_s = 0
PumpTwoStatus_s = 0
PressureValue_s = 0
PressureValue_f = 0
pHValue_s = 0
pHValue_f = 0
SERIALOBJECT = None  # Global variable for the data from the serial port.
ConnectRequest = None
Feedback = None
CoolingONRequest = None
CoolingOFFRequest = None
PerfusionONRequest = None
PerfusionOFFRequest = None
DryIceTareRequest = None
PerfusionFluidTareRequest = None
WasteFluidTareRequest = None
ExhaustONRequest = None
ExhaustOFFRequest = None
UpdatePerfusionSettingsRequest = None
Motor1ForwardONRequest = None
Motor1ForwardOFFRequest = None
Motor2ForwardONRequest = None
Motor2ForwardOFFRequest = None
Motor1BackwardONRequest = None
Motor1BackwardOFFRequest = None
Motor2BackwardONRequest = None
Motor2BackwardOFFRequest = None
ResetPerfusionDataRequest = None
NumOfPerfusionCycles_s = None
NumOfPerfusionCycles_f = 0
FlowRate = 0
TimeInterval = 0
index1 = 0
index2 = 0
index3 = 0
otf = 0
patchFlag=0
"""
Patch timer is run periodically
"""

x = list()
x_time = list()
y = list()
TopTemperatureList = list()
BottomTemperatureList = list()
HeartTemperatureList = list()
DryIceList = list()
SetPoint1List = list()
SetPoint2List = list()
rows = list()
BlowerPIDOutputList = list()
BlowerPWMOutputList = list()
BlowerOnOffList = list()
ExhaustOnOffList = list()
PressureList = list()
pHValueList = list()
i = 0
Time_i = 0
TriggerPlotting = False
TriggerDataLog = False
# field names
fields = ['Sl.No.', 'Time', 'Top Temperature', 'Bottom Temperature', 'Average Temperature', 'Heart  Temperature', 'DryIce Units', 'BlowerPIDOutput', 'BlowerFunctionalTime', 'BlowerOnOff', 'ExhaustOnOff', 'Pressure', 'pH']
# name of csv file
filename = "records.csv"


class Ui_MyGUI(object):
    global ConnectRequest
    

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_18 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_18.setGeometry(QtCore.QRect(600, 330, 191, 141))
        self.groupBox_18.setStyleSheet("background-color: rgb(228, 255, 255)")
        self.groupBox_18.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_18.setObjectName("groupBox_18")
        self.widget = QtWidgets.QWidget(self.groupBox_18)
        self.widget.setGeometry(QtCore.QRect(10, 20, 172, 61))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Motor1ForwardOnOffButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.Motor1ForwardOnOffButton.setFont(font)
        self.Motor1ForwardOnOffButton.setStyleSheet("background-color: rgb(252, 238, 255);\n"
                                                    "color: black; \n"
                                                    "border-radius: 10px; border: 2px groove gray;\n"
                                                    "border-style: outset;")
        self.Motor1ForwardOnOffButton.setCheckable(True)
        self.Motor1ForwardOnOffButton.setObjectName("Motor1ForwardOnOffButton")
        self.horizontalLayout.addWidget(self.Motor1ForwardOnOffButton)
        self.Motor1BackwardOnOffButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.Motor1BackwardOnOffButton.setFont(font)
        self.Motor1BackwardOnOffButton.setStyleSheet("background-color: rgb(252, 238, 255);\n"
                                                     "color: black; \n"
                                                     "border-radius: 10px; border: 2px groove gray;\n"
                                                     "border-style: outset;")
        self.Motor1BackwardOnOffButton.setCheckable(True)
        self.Motor1BackwardOnOffButton.setObjectName("Motor1BackwardOnOffButton")
        self.horizontalLayout.addWidget(self.Motor1BackwardOnOffButton)
        self.widget1 = QtWidgets.QWidget(self.groupBox_18)
        self.widget1.setGeometry(QtCore.QRect(10, 80, 172, 61))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Motor2ForwardOnOffButton = QtWidgets.QPushButton(self.widget1)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.Motor2ForwardOnOffButton.setFont(font)
        self.Motor2ForwardOnOffButton.setStyleSheet("background-color: rgb(252, 238, 255);\n"
                                                    "color: black; \n"
                                                    "border-radius: 10px; border: 2px groove gray;\n"
                                                    "border-style: outset;")
        self.Motor2ForwardOnOffButton.setCheckable(True)
        self.Motor2ForwardOnOffButton.setObjectName("Motor2ForwardOnOffButton")
        self.horizontalLayout_2.addWidget(self.Motor2ForwardOnOffButton)
        self.Motor2BackwardOnOffButton = QtWidgets.QPushButton(self.widget1)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.Motor2BackwardOnOffButton.setFont(font)
        self.Motor2BackwardOnOffButton.setStyleSheet("background-color: rgb(252, 238, 255);\n"
                                                     "color: black; \n"
                                                     "border-radius: 10px; border: 2px groove gray;\n"
                                                     "border-style: outset;")
        self.Motor2BackwardOnOffButton.setCheckable(True)
        self.Motor2BackwardOnOffButton.setObjectName("Motor2BackwardOnOffButton")
        self.horizontalLayout_2.addWidget(self.Motor2BackwardOnOffButton)
        self.groupBox_22 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_22.setGeometry(QtCore.QRect(210, 350, 181, 121))
        self.groupBox_22.setStyleSheet("background-color: rgb(228, 255, 255);")
        self.groupBox_22.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_22.setObjectName("groupBox_22")
        self.widget2 = QtWidgets.QWidget(self.groupBox_22)
        self.widget2.setGeometry(QtCore.QRect(11, 24, 161, 61))
        self.widget2.setObjectName("widget2")
        self.gridLayout_22 = QtWidgets.QGridLayout(self.widget2)
        self.gridLayout_22.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_22.setObjectName("gridLayout_22")
        self.ExitButton = QtWidgets.QPushButton(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ExitButton.setFont(font)
        self.ExitButton.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                      "color: black; \n"
                                      "border-radius: 10px; border: 2px groove gray;\n"
                                      "border-style: outset;\n"
                                      "\n"
                                      "")
        self.ExitButton.setCheckable(True)
        self.ExitButton.setObjectName("ExitButton")
        self.gridLayout_22.addWidget(self.ExitButton, 2, 0, 1, 1)
        self.Button = QtWidgets.QPushButton(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Button.setFont(font)
        self.Button.setStyleSheet("background-color: rgb(0, 255, 100);\n"
                                  "color: black; \n"
                                  "border-radius: 10px; border: 2px groove gray;\n"
                                  "border-style: outset;")
        self.Button.setCheckable(True)
        self.Button.setObjectName("Button")
        self.gridLayout_22.addWidget(self.Button, 1, 0, 1, 1)
        self.groupBox_13 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_13.setGeometry(QtCore.QRect(400, 10, 191, 461))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_13.setFont(font)
        self.groupBox_13.setStyleSheet("background-color: rgb(228, 255, 255);")
        self.groupBox_13.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_13.setObjectName("groupBox_13")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.groupBox_13)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.UpdatePerfusionSettingButton = QtWidgets.QPushButton(self.groupBox_13)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.UpdatePerfusionSettingButton.setFont(font)
        self.UpdatePerfusionSettingButton.setStyleSheet("background-color: rgb(255, 0, 100);\n"
                                                        "color: black; \n"
                                                        "border-radius: 5px; border: 2px groove gray;\n"
                                                        "border-style: outset;")
        self.UpdatePerfusionSettingButton.setObjectName("UpdatePerfusionSettingButton")
        self.gridLayout_11.addWidget(self.UpdatePerfusionSettingButton, 6, 0, 1, 1)
        self.StartStopPerfusionButton = QtWidgets.QPushButton(self.groupBox_13)
        self.StartStopPerfusionButton.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.StartStopPerfusionButton.setFont(font)
        self.StartStopPerfusionButton.setStyleSheet("color: black; \n"
                                                    "border-radius: 5px; border: 2px groove gray;\n"
                                                    "border-style: outset;")
        self.StartStopPerfusionButton.setCheckable(True)
        self.StartStopPerfusionButton.setObjectName("StartStopPerfusionButton")
        self.gridLayout_11.addWidget(self.StartStopPerfusionButton, 7, 0, 1, 1)
        self.groupBox_14 = QtWidgets.QGroupBox(self.groupBox_13)
        self.groupBox_14.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_14.setObjectName("groupBox_14")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.groupBox_14)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.FlowRateCB = QtWidgets.QComboBox(self.groupBox_14)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.FlowRateCB.setFont(font)
        self.FlowRateCB.setObjectName("FlowRateCB")
        self.FlowRateCB.addItem("")
        self.FlowRateCB.addItem("")
        self.FlowRateCB.addItem("")
        self.FlowRateCB.addItem("")
        self.FlowRateCB.addItem("")
        self.FlowRateCB.addItem("")
        self.FlowRateCB.addItem("")
        self.gridLayout_12.addWidget(self.FlowRateCB, 1, 1, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox_14, 0, 0, 1, 1)
        self.groupBox_16 = QtWidgets.QGroupBox(self.groupBox_13)
        self.groupBox_16.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_16.setObjectName("groupBox_16")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.groupBox_16)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.PerfusionTimeCB = QtWidgets.QComboBox(self.groupBox_16)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.PerfusionTimeCB.setFont(font)
        self.PerfusionTimeCB.setObjectName("PerfusionTimeCB")
        self.PerfusionTimeCB.addItem("")
        self.PerfusionTimeCB.addItem("")
        self.PerfusionTimeCB.addItem("")
        self.PerfusionTimeCB.addItem("")
        self.PerfusionTimeCB.addItem("")
        self.PerfusionTimeCB.addItem("")
        self.PerfusionTimeCB.addItem("")
        self.PerfusionTimeCB.addItem("")
        self.PerfusionTimeCB.addItem("")
        self.gridLayout_14.addWidget(self.PerfusionTimeCB, 0, 1, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox_16, 2, 0, 1, 1)
        self.groupBox_15 = QtWidgets.QGroupBox(self.groupBox_13)
        self.groupBox_15.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_15.setObjectName("groupBox_15")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.groupBox_15)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.IntervalCB = QtWidgets.QComboBox(self.groupBox_15)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.IntervalCB.setFont(font)
        self.IntervalCB.setObjectName("IntervalCB")
        self.IntervalCB.addItem("")
        self.IntervalCB.addItem("")
        self.IntervalCB.addItem("")
        self.IntervalCB.addItem("")
        self.IntervalCB.addItem("")
        self.IntervalCB.addItem("")
        self.IntervalCB.addItem("")
        self.IntervalCB.addItem("")
        self.IntervalCB.addItem("")
        self.IntervalCB.addItem("")
        self.gridLayout_13.addWidget(self.IntervalCB, 1, 1, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox_15, 3, 0, 1, 1)
        self.groupBox_20 = QtWidgets.QGroupBox(self.groupBox_13)
        self.groupBox_20.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_20.setObjectName("groupBox_20")
        self.gridLayout_19 = QtWidgets.QGridLayout(self.groupBox_20)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.PressureLCD = QtWidgets.QLCDNumber(self.groupBox_20)
        self.PressureLCD.setDigitCount(4)
        self.PressureLCD.setObjectName("PressureLCD")
        self.gridLayout_19.addWidget(self.PressureLCD, 0, 0, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox_20, 4, 0, 1, 1)
        self.groupBox_21 = QtWidgets.QGroupBox(self.groupBox_13)
        self.groupBox_21.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_21.setObjectName("groupBox_21")
        self.gridLayout_20 = QtWidgets.QGridLayout(self.groupBox_21)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.pHLCD = QtWidgets.QLCDNumber(self.groupBox_21)
        self.pHLCD.setDigitCount(4)
        self.pHLCD.setObjectName("pHLCD")
        self.gridLayout_20.addWidget(self.pHLCD, 0, 0, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox_21, 5, 0, 1, 1)
        self.ResetPerusionButton = QtWidgets.QPushButton(self.groupBox_13)
        self.ResetPerusionButton.setStyleSheet("color: black; \n"
                                               "border-radius: 5px; border: 2px groove gray;\n"
                                               "border-style: outset;")
        self.ResetPerusionButton.setObjectName("ResetPerusionButton")
        self.gridLayout_11.addWidget(self.ResetPerusionButton, 8, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(210, 10, 181, 331))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setStyleSheet("background-color: rgb(228, 255, 255);")
        self.groupBox_4.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.groupBox_10 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_10.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_10.setObjectName("groupBox_10")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_10)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.Count5lcdNum = QtWidgets.QLCDNumber(self.groupBox_10)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Count5lcdNum.setFont(font)
        self.Count5lcdNum.setAutoFillBackground(False)
        self.Count5lcdNum.setDigitCount(4)
        self.Count5lcdNum.setProperty("value", 0.0)
        self.Count5lcdNum.setObjectName("Count5lcdNum")
        self.gridLayout_6.addWidget(self.Count5lcdNum, 1, 1, 1, 1)
        self.DryIceTareButton = QtWidgets.QPushButton(self.groupBox_10)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.DryIceTareButton.setFont(font)
        self.DryIceTareButton.setCheckable(True)
        self.DryIceTareButton.setObjectName("DryIceTareButton")
        self.gridLayout_6.addWidget(self.DryIceTareButton, 2, 1, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_10, 0, 0, 1, 1)
        self.groupBox_11 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_11.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_11.setObjectName("groupBox_11")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_11)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.Count5lcdNum_2 = QtWidgets.QLCDNumber(self.groupBox_11)
        self.Count5lcdNum_2.setAutoFillBackground(False)
        self.Count5lcdNum_2.setDigitCount(4)
        self.Count5lcdNum_2.setProperty("value", 0.0)
        self.Count5lcdNum_2.setObjectName("Count5lcdNum_2")
        self.gridLayout_8.addWidget(self.Count5lcdNum_2, 2, 0, 1, 1)
        self.PerfusionFluidTareButton = QtWidgets.QPushButton(self.groupBox_11)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.PerfusionFluidTareButton.setFont(font)
        self.PerfusionFluidTareButton.setCheckable(True)
        self.PerfusionFluidTareButton.setObjectName("PerfusionFluidTareButton")
        self.gridLayout_8.addWidget(self.PerfusionFluidTareButton, 3, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_11, 1, 0, 1, 1)
        self.groupBox_12 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_12.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_12.setObjectName("groupBox_12")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.groupBox_12)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.WasteFluidTareButton = QtWidgets.QPushButton(self.groupBox_12)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.WasteFluidTareButton.setFont(font)
        self.WasteFluidTareButton.setCheckable(True)
        self.WasteFluidTareButton.setObjectName("WasteFluidTareButton")
        self.gridLayout_9.addWidget(self.WasteFluidTareButton, 1, 0, 1, 1)
        self.Count5lcdNum_3 = QtWidgets.QLCDNumber(self.groupBox_12)
        self.Count5lcdNum_3.setAutoFillBackground(False)
        self.Count5lcdNum_3.setDigitCount(4)
        self.Count5lcdNum_3.setProperty("value", 0.0)
        self.Count5lcdNum_3.setObjectName("Count5lcdNum_3")
        self.gridLayout_9.addWidget(self.Count5lcdNum_3, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_12, 2, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(600, 10, 191, 311))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setStyleSheet("background-color: rgb(228, 255, 255);")
        self.groupBox_3.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_17 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.groupBox_9 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_9.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_9.setObjectName("groupBox_9")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_9)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.Count5lcdNum_4 = QtWidgets.QLCDNumber(self.groupBox_9)
        self.Count5lcdNum_4.setAutoFillBackground(False)
        self.Count5lcdNum_4.setDigitCount(4)
        self.Count5lcdNum_4.setProperty("value", 0.0)
        self.Count5lcdNum_4.setObjectName("Count5lcdNum_4")
        self.gridLayout_5.addWidget(self.Count5lcdNum_4, 0, 0, 1, 1)
        self.gridLayout_17.addWidget(self.groupBox_9, 0, 0, 1, 1)
        self.groupBox_19 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_19.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_19.setObjectName("groupBox_19")
        self.label_8 = QtWidgets.QLabel(self.groupBox_19)
        self.label_8.setGeometry(QtCore.QRect(20, 20, 131, 20))
        self.label_8.setStyleSheet("background-color: rgb(255, 255, 200);")
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox_19)
        self.label_9.setGeometry(QtCore.QRect(20, 40, 131, 21))
        self.label_9.setStyleSheet("background-color: rgb(255, 255, 200);")
        self.label_9.setObjectName("label_9")
        self.gridLayout_17.addWidget(self.groupBox_19, 3, 0, 1, 1)
        self.groupBox_17 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_17.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_17.setObjectName("groupBox_17")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.groupBox_17)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.testLabel=QtWidgets.QLabel(self.groupBox_17)
        self.testLabel.setAutoFillBackground(False)
        #self.testLabel.setVisible(False)
        self.testLabel.setText('0.0')
        
        self.Count5lcdNum_5 = QtWidgets.QLCDNumber(self.groupBox_17)
        self.Count5lcdNum_5.setAutoFillBackground(False)
        self.Count5lcdNum_5.setDigitCount(4)
        self.Count5lcdNum_5.setProperty("value", 0.0)
        self.Count5lcdNum_5.setObjectName("Count5lcdNum_5")
        self.gridLayout_15.addWidget(self.Count5lcdNum_5, 0, 0, 1, 1)
        self.gridLayout_17.addWidget(self.groupBox_17, 1, 0, 1, 1)
        self.groupBox_23 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_23.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_23.setObjectName("groupBox_23")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.groupBox_23)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.Count5lcdNum_6 = QtWidgets.QLCDNumber(self.groupBox_23)
        self.Count5lcdNum_6.setAutoFillBackground(False)
        self.Count5lcdNum_6.setDigitCount(4)
        self.Count5lcdNum_6.setProperty("value", 0.0)
        self.Count5lcdNum_6.setObjectName("Count5lcdNum_6")
        self.gridLayout_16.addWidget(self.Count5lcdNum_6, 0, 0, 1, 1)
        self.gridLayout_17.addWidget(self.groupBox_23, 2, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(11, 11, 191, 461))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("background-color: rgb(228, 255, 255);")
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_18 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.CoolingOnOffButton = QtWidgets.QPushButton(self.groupBox_2)
        self.CoolingOnOffButton.setGeometry(QtCore.QRect(10, 350, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.CoolingOnOffButton.setFont(font)
        self.CoolingOnOffButton.setStyleSheet("background-color: rgb(255, 0, 100);\n"
                                              "color: black; \n"
                                              "border-radius: 10px; border: 2px groove gray;\n"
                                              "border-style: outset;")
        self.CoolingOnOffButton.setCheckable(True)
        self.CoolingOnOffButton.setObjectName("CoolingOnOffButton")
        self.ExhaustOnOffButton = QtWidgets.QPushButton(self.groupBox_2)
        self.ExhaustOnOffButton.setGeometry(QtCore.QRect(10, 390, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.ExhaustOnOffButton.setFont(font)
        self.ExhaustOnOffButton.setStyleSheet("background-color: rgb(255, 0, 100);\n"
                                              "color: black; \n"
                                              "border-radius: 10px; border: 2px groove gray;\n"
                                              "border-style: outset;")
        self.ExhaustOnOffButton.setCheckable(True)
        self.ExhaustOnOffButton.setObjectName("ExhaustOnOffButton")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(10, 30, 149, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.widget3 = QtWidgets.QWidget(self.groupBox_2)
        self.widget3.setGeometry(QtCore.QRect(10, 60, 167, 281))
        self.widget3.setObjectName("widget3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_5 = QtWidgets.QGroupBox(self.widget3)
        self.groupBox_5.setStyleSheet("")
        self.groupBox_5.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout.setObjectName("gridLayout")
        self.Count1lcdNum = QtWidgets.QLCDNumber(self.groupBox_5)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Count1lcdNum.setFont(font)
        self.Count1lcdNum.setDigitCount(4)
        self.Count1lcdNum.setObjectName("Count1lcdNum")
        self.gridLayout.addWidget(self.Count1lcdNum, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.groupBox_6 = QtWidgets.QGroupBox(self.widget3)
        self.groupBox_6.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Count2lcdNum = QtWidgets.QLCDNumber(self.groupBox_6)
        self.Count2lcdNum.setDigitCount(4)
        self.Count2lcdNum.setObjectName("Count2lcdNum")
        self.gridLayout_2.addWidget(self.Count2lcdNum, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_6)
        self.groupBox_7 = QtWidgets.QGroupBox(self.widget3)
        self.groupBox_7.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_7.setObjectName("groupBox_7")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_7)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Count3lcdNum = QtWidgets.QLCDNumber(self.groupBox_7)
        self.Count3lcdNum.setDigitCount(4)
        self.Count3lcdNum.setObjectName("Count3lcdNum")
        self.gridLayout_3.addWidget(self.Count3lcdNum, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_7)
        self.groupBox_8 = QtWidgets.QGroupBox(self.widget3)
        self.groupBox_8.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_8.setObjectName("groupBox_8")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_8)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.Count4lcdNum = QtWidgets.QLCDNumber(self.groupBox_8)
        self.Count4lcdNum.setDigitCount(4)
        self.Count4lcdNum.setObjectName("Count4lcdNum")
        self.gridLayout_4.addWidget(self.Count4lcdNum, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_8)
        self.gridLayout_18.addWidget(self.groupBox_2, 0, 0, 1, 1)
        
        
        """
        Dummy button
        """
        self.dummyButton = QtWidgets.QPushButton(self.widget2)
        self.dummyButton.setVisible(False)
        self.dummyButton.clicked.connect(lambda v:print("Dummy clicked"))
        
        
        MainWindow.setCentralWidget(self.centralwidget)

        x.append(i)
        x_time.append(i)
        y.append(AverageTemperature_s)  # Temperature data
        TopTemperatureList.append(TopTemperature_s)
        BottomTemperatureList.append(BottomTemperature_s)
        HeartTemperatureList.append(HeartTemperature_s)
        DryIceList.append(DryIceLoad_s)
        BlowerPIDOutputList.append(BlowerPIDOutput_s)
        BlowerPWMOutputList.append(BlowerPWM_s)
        BlowerOnOffList.append(Blower_On_Off_s)
        ExhaustOnOffList.append(Exhaust_On_Off_s)
        PressureList.append(PressureValue_s)
        pHValueList.append(pHValue_s)
        SetPoint1 = 2
        SetPoint2 = 8
        SetPoint1List.append(SetPoint1)
        SetPoint2List.append(SetPoint2)
        
        
        
        # self.graphicsView.setBackground('k')
        # self.graphicsView.setTitle("Temperature Feedback", color="w", size="16pt")
        # styles = {"color": "#fff", "font-size": "12pt"}
        # self.graphicsView.showGrid(x=True, y=True)
        # self.graphicsView.setLabel('left', 'Temperature (°C)', **styles)
        # self.graphicsView.setLabel('bottom', 'Time (Sec)', **styles)

        # SetPointPen = pg.mkPen(color=(0, 0, 255))
        # self.SetPoint_line = self.graphicsView.plot(x, SetPointList, pen=SetPointPen, )
        # AvgTempPen = pg.mkPen(color=(0, 255, 0))
        # self.AvgTemp_line = self.graphicsView.plot(x, y, pen=AvgTempPen, )
        # self.graphicsView.addLegend()

        # pen = pg.mkPen(color='g')
        # self.graphicsView.plot(x, y, name="Average Temp", pen=pen, )
        # pen = pg.mkPen(color='r')
        # self.graphicsView.plot(x, SetPoint1List, name="SetPoint Temp 1", pen=pen, )
        # pen = pg.mkPen(color='r')
        # self.graphicsView.plot(x, SetPoint2List, name="SetPoint Temp 2", pen=pen, )
        # pen = pg.mkPen(color='y')
        # self.graphicsView.plot(x, TopTemperatureList, name="Top Temp", pen=pen, )
        # pen = pg.mkPen(color='c')
        # self.graphicsView.plot(x, BottomTemperatureList, name="Bottom Temp", pen=pen, )
        # pen = pg.mkPen(color='m')
        # self.graphicsView.plot(x, HeartTemperatureList, name="Heart Temp", pen=pen, )

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_data_log)
        # self.plot_timer = QtCore.QTimer()
        # self.plot_timer.setInterval(1000)
        # self.plot_timer.timeout.connect(self.update_data_plot)

        # writing to csv file
        with open(filename, 'w', newline='') as csvfile:
            csvfile.flush()
            # creating a csv writer object
            csvwriter = csv.writer(csvfile, dialect='excel')

            # writing the fields
            csvwriter.writerow(fields)

            csvfile.close()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.Button.toggled.connect(self.on_toggled)
        self.CoolingOnOffButton.toggled.connect(self.cooling_on_off)
        self.DryIceTareButton.clicked.connect(self.DryIceTare)
        self.ExhaustOnOffButton.toggled.connect(self.exhaust_on_off)
        self.ExitButton.clicked.connect(self.exit)
        self.PerfusionFluidTareButton.toggled.connect(self.PerfusionFluidTare)
        self.WasteFluidTareButton.toggled.connect(self.WasteFluidTare)
        self.StartStopPerfusionButton.toggled.connect(self.StartStopPerfusion)
        self.UpdatePerfusionSettingButton.clicked.connect(self.UpdatePerfusionSettings)
        self.Motor1ForwardOnOffButton.toggled.connect(self.motor_1_forward_on_off)
        self.Motor1BackwardOnOffButton.toggled.connect(self.motor_1_backward_on_off)
        self.Motor2ForwardOnOffButton.toggled.connect(self.motor_2_forward_on_off)
        self.Motor2BackwardOnOffButton.toggled.connect(self.motor_2_backward_on_off)
        self.ResetPerusionButton.clicked.connect(self.reset_perfusion_data)
        
        """
        Data correction timer
        """
        self.dataCorrectionTimer=QTimer()
        self.dataCorrectionTimer.timeout.connect(self.patchSignal)
    
    
    def patchSignal(self):
        global patchFlag
        patchFlag=1
        
        
    def plot(self, x, y, color):
        pen = pg.mkPen(color=color)
        self.graphicsView.plot(x, y, pen=pen, )

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_18.setTitle(_translate("MainWindow", "DEBUG Controls"))
        self.Motor1ForwardOnOffButton.setText(_translate("MainWindow", "Motor 1\n"
                                                                       "Forward ON"))
        self.Motor1BackwardOnOffButton.setText(_translate("MainWindow", "Motor 1\n"
                                                                        "Backward ON"))
        self.Motor2ForwardOnOffButton.setText(_translate("MainWindow", "Motor 2\n"
                                                                       "Forward ON"))
        self.Motor2BackwardOnOffButton.setText(_translate("MainWindow", "Motor 2\n"
                                                                        "Backward ON"))
        self.groupBox_22.setTitle(_translate("MainWindow", "Connection"))
        self.ExitButton.setText(_translate("MainWindow", "EXIT"))
        self.Button.setText(_translate("MainWindow", "CONNECT"))
        self.groupBox_13.setTitle(_translate("MainWindow", "Perfusion Control"))
        self.UpdatePerfusionSettingButton.setText(_translate("MainWindow", "Update Settings"))
        self.StartStopPerfusionButton.setText(_translate("MainWindow", "START Perfusion"))
        self.groupBox_14.setTitle(_translate("MainWindow", "Perfusion flow rate (mL/min)"))
        self.FlowRateCB.setCurrentText(_translate("MainWindow", "Select Flow Rate"))
        self.FlowRateCB.setItemText(0, _translate("MainWindow", "Select Flow Rate"))
        self.FlowRateCB.setItemText(1, _translate("MainWindow", "100"))
        self.FlowRateCB.setItemText(2, _translate("MainWindow", "150"))
        self.FlowRateCB.setItemText(3, _translate("MainWindow", "200"))
        self.FlowRateCB.setItemText(4, _translate("MainWindow", "250"))
        self.FlowRateCB.setItemText(5, _translate("MainWindow", "300"))
        self.FlowRateCB.setItemText(6, _translate("MainWindow", "None"))
        self.groupBox_16.setTitle(_translate("MainWindow", "Perfusion time (seconds)"))
        self.PerfusionTimeCB.setItemText(0, _translate("MainWindow", "Select Time     "))
        self.PerfusionTimeCB.setItemText(1, _translate("MainWindow", "30"))
        self.PerfusionTimeCB.setItemText(2, _translate("MainWindow", "45"))
        self.PerfusionTimeCB.setItemText(3, _translate("MainWindow", "60"))
        self.PerfusionTimeCB.setItemText(4, _translate("MainWindow", "75"))
        self.PerfusionTimeCB.setItemText(5, _translate("MainWindow", "90"))
        self.PerfusionTimeCB.setItemText(6, _translate("MainWindow", "105"))
        self.PerfusionTimeCB.setItemText(7, _translate("MainWindow", "120"))
        self.PerfusionTimeCB.setItemText(8, _translate("MainWindow", "None"))
        self.groupBox_15.setTitle(_translate("MainWindow", "Perfusion Interval (minutes)"))
        self.IntervalCB.setItemText(0, _translate("MainWindow", "Select Time     "))
        self.IntervalCB.setItemText(1, _translate("MainWindow", "3"))
        self.IntervalCB.setItemText(2, _translate("MainWindow", "10"))
        self.IntervalCB.setItemText(3, _translate("MainWindow", "15"))
        self.IntervalCB.setItemText(4, _translate("MainWindow", "20"))
        self.IntervalCB.setItemText(5, _translate("MainWindow", "25"))
        self.IntervalCB.setItemText(6, _translate("MainWindow", "30"))
        self.IntervalCB.setItemText(7, _translate("MainWindow", "35"))
        self.IntervalCB.setItemText(8, _translate("MainWindow", "40"))
        self.IntervalCB.setItemText(9, _translate("MainWindow", "None"))
        self.groupBox_20.setTitle(_translate("MainWindow", "In-Line Pressure (mmHg)"))
        self.groupBox_21.setTitle(_translate("MainWindow", "pH (0-14)"))
        self.ResetPerusionButton.setText(_translate("MainWindow", "RESET"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Loadcell Feedbacks"))
        self.groupBox_10.setTitle(_translate("MainWindow", "Dry ice (grams)"))
        self.DryIceTareButton.setText(_translate("MainWindow", "TARE"))
        self.groupBox_11.setTitle(_translate("MainWindow", "Saline bag 1 (grams)"))
        self.PerfusionFluidTareButton.setText(_translate("MainWindow", "TARE"))
        self.groupBox_12.setTitle(_translate("MainWindow", "Saline bag 2 (grams)"))
        self.WasteFluidTareButton.setText(_translate("MainWindow", "TARE"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Time"))
        self.groupBox_9.setTitle(_translate("MainWindow", "Total time elapsed (Seconds)"))
        self.groupBox_19.setTitle(_translate("MainWindow", "Motor Status"))
        self.groupBox_17.setTitle(_translate("MainWindow", "Time until next perfusion(seconds)"))
        self.groupBox_23.setTitle(_translate("MainWindow", "No. of perfusion cycles completed"))
        self.groupBox.setTitle(_translate("MainWindow", "Cooling Control"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Temperature Feedbacks"))
        self.CoolingOnOffButton.setText(_translate("MainWindow", "COOLING ON"))
        self.ExhaustOnOffButton.setText(_translate("MainWindow", "OPEN EXHAUST"))
        self.label_3.setText(_translate("MainWindow", "Set Point = 6"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Top Temperature (°C)"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Bottom Temperature (°C)"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Average Temperature (°C)"))
        self.groupBox_8.setTitle(_translate("MainWindow", "Heart Temperature (°C)"))

    def exit(self):
        self.timer.stop()
        sys.exit()

    def on_toggled(self, checked):
        global ConnectRequest
        global Plotting_Thread
        self.Button.setText("DISCONNECT" if checked else "CONNECT")
        if checked:  # Connect Clicked
            ConnectRequest = 1
            self.timer.start()
            # self.plot_timer.start()
            # Plotting_Thread.start()  # Start the Plotting thread.
            self.dataCorrectionTimer.start(1000)

        else:  # DisConnect Clicked
            self.dataCorrectionTimer.stop()
            ConnectRequest = 2
            self.timer.stop()
            # self.plot_timer.stop()
            self.update_data_log()
            # self.update_data_plot()
            # ex = pg.exporters.ImageExporter(self.graphicsView.scene())
            # ex.export("test.png")

    def cooling_on_off(self, checked):
        global CoolingONRequest
        global CoolingOFFRequest
        self.CoolingOnOffButton.setText("COOLING OFF" if checked else "COOLING ON")
        if checked:  # COOLING ON Clicked
            CoolingONRequest = 1
            CoolingOFFRequest = 0
        else:  # COOLING OFF Clicked
            CoolingONRequest = 0
            CoolingOFFRequest = 1

    def UpdatePerfusionSettings(self):
        global UpdatePerfusionSettingsRequest
        global FlowRate
        global TimeInterval
        global index1
        global index2
        global index3
        global otf
        index1 = self.FlowRateCB.currentIndex()
        index2 = self.IntervalCB.currentIndex()
        index3 = self.PerfusionTimeCB.currentIndex()
        if index2 == 1:
            TimeInterval = 3 * 60
        elif index2 == 2:
            TimeInterval = 10 * 60
        elif index2 == 3:
            TimeInterval = 15 * 60
        elif index2 == 4:
            TimeInterval = 20 * 60
        elif index2 == 5:
            TimeInterval = 25 * 60
        elif index2 == 6:
            TimeInterval = 30 * 60
        elif index2 == 7:
            TimeInterval = 35 * 60
        elif index2 == 8:
            TimeInterval = 40 * 60
        else:
            pass

        print("index1 FlowRateCB = ", index1)
        print("index2 IntervalCB = ", index2)
        print("index3 PerfusionTimeCB = ", index3)
        otf = 1
        UpdatePerfusionSettingsRequest = 1

    def StartStopPerfusion(self, checked):
        global PerfusionONRequest
        global PerfusionOFFRequest        
        #self.gif.start()
        self.StartStopPerfusionButton.setText("STOP PERFUSION" if checked else "START PERFUSION ")
        if checked:  # Perfusion ON Clicked
            PerfusionONRequest = 1
            PerfusionOFFRequest = 0
        else:  # Perfusion OFF Clicked
            PerfusionONRequest = 0
            PerfusionOFFRequest = 1
            self.StartStopPerfusionButton.setEnabled(False)

    def DryIceTare(self, checked):
        global DryIceTareRequest
        DryIceTareRequest = 1

    def PerfusionFluidTare(self, checked):
        global PerfusionFluidTareRequest
        PerfusionFluidTareRequest = 1

    def WasteFluidTare(self, checked):
        global WasteFluidTareRequest
        WasteFluidTareRequest = 1

    def exhaust_on_off(self, checked):
        global ExhaustONRequest
        global ExhaustOFFRequest
        self.ExhaustOnOffButton.setText("EXHAUST OFF" if checked else "EXHAUST ON")
        if checked:  # EXHAUST ON Clicked
            ExhaustONRequest = 1
            ExhaustOFFRequest = 0
        else:  # EXHAUST OFF Clicked
            ExhaustONRequest = 0
            ExhaustOFFRequest = 1

    def motor_1_forward_on_off(self, checked):
        global Motor1ForwardONRequest
        global Motor1ForwardOFFRequest
        self.Motor1ForwardOnOffButton.setText("Motor 1 \nForward OFF" if checked else "Motor 1 \nForward ON")
        if checked:  # Motor 1 ON Clicked
            Motor1ForwardONRequest = 1
            Motor1ForwardOFFRequest = 0
        else:  # Motor 1 OFF Clicked
            Motor1ForwardONRequest = 0
            Motor1ForwardOFFRequest = 1

    def motor_2_forward_on_off(self, checked):
        global Motor2ForwardONRequest
        global Motor2ForwardOFFRequest
        self.Motor2ForwardOnOffButton.setText("Motor 2 \nForward OFF" if checked else "Motor 2 \nForward ON")
        if checked:  # Motor 2 ON Clicked
            Motor2ForwardONRequest = 1
            Motor2ForwardOFFRequest = 0
        else:  # Motor 2 OFF Clicked
            Motor2ForwardONRequest = 0
            Motor2ForwardOFFRequest = 1

    def motor_1_backward_on_off(self, checked):
        global Motor1BackwardONRequest
        global Motor1BackwardOFFRequest
        self.Motor1BackwardOnOffButton.setText("Motor 1 \nBackward OFF" if checked else "Motor 1 \nBackward ON")
        if checked:  # Motor 1 ON Clicked
            Motor1BackwardONRequest = 1
            Motor1BackwardOFFRequest = 0
        else:  # Motor 1 OFF Clicked
            Motor1BackwardONRequest = 0
            Motor1BackwardOFFRequest = 1

    def motor_2_backward_on_off(self, checked):
        global Motor2BackwardONRequest
        global Motor2BackwardOFFRequest
        self.Motor2BackwardOnOffButton.setText("Motor 2 \nBackward OFF" if checked else "Motor 2 \nBackward ON")
        if checked:  # Motor 2 ON Clicked
            Motor2BackwardONRequest = 1
            Motor2BackwardOFFRequest = 0
        else:  # Motor 2 OFF Clicked
            Motor2BackwardONRequest = 0
            Motor2BackwardOFFRequest = 1

    def reset_perfusion_data(self):
        global ResetPerfusionDataRequest
        ResetPerfusionDataRequest = 1
        otf = 0


    def update_data_log(self):
        global AverageTemperature  # Use global variable AverageTemperature
        global TopTemperature  # Use global variable TopTemperature
        global BottomTemperature  # Use global variable BottomTemperature
        global HeartTemperature  # Use global variable HeartTemperature
        global DryIce  # Use global variable DryIce
        global BlowerPWM  # Use global variable BlowerPWM
        global TopTemperatureList
        global BottomTemperatureList
        global HeartTemperatureList
        global DryIceList
        global BlowerPIDOutputList
        global BlowerPWMOutputList
        global BlowerOnOffList
        global ExhaustOnOffList
        global PressureList
        global pHValueList
        global SetPoint1List
        global SetPoint2List
        global x
        global x_time
        global y
        global i
        global TriggerPlotting
        global TriggerDataLog
        global Time_i
        global TopTemperature_s
        global TopTemperature_f
        global BottomTemperature_s
        global BottomTemperature_f
        global AverageTemperature_s
        global AverageTemperature_f
        global HeartTemperature_s
        global HeartTemperature_f
        global DryIceLoad_s
        global DryIceLoad_f
        global SalineOneLoad_s
        global SalineOneLoad_f
        global SalineTwoLoad_s
        global SalineTwoLoad_f
        global BlowerPWM_s
        global BlowerPWM_f
        global BlowerPIDOutput_s
        global BlowerPIDOutput_f
        global Blower_On_Off_s
        global Blower_On_Off_f
        global Exhaust_On_Off_s
        global Exhaust_On_Off_f
        global PumpOneStatus_s
        global PumpTwoStatus_s
        global GsecCounter_s
        global GsecCounter_f
        global SecondCount_s
        global SecondCount_f
        global PressureValue_s
        global PressureValue_f
        global pHValue_s
        global pHValue_f
        global rows

        TriggerDataLog = True
        TriggerPlotting = True
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        i = i + 1
        Time_i = Time_i + 1

        # if Time_i % 5 == 0:
        #     Time_i = 0
        #     TriggerPlotting = True
        # else:
        #     TriggerPlotting = False
        x.append(i)
        x_time.append(current_time)
        y.append(AverageTemperature_s)  # Temperature data
        TopTemperatureList.append(TopTemperature_s)
        BottomTemperatureList.append(BottomTemperature_s)
        HeartTemperatureList.append(HeartTemperature_s)
        DryIceList.append(DryIceLoad_s)
        BlowerPIDOutputList.append(BlowerPIDOutput_s)
        BlowerPWMOutputList.append(BlowerPWM_s)
        BlowerOnOffList.append(Blower_On_Off_s)
        ExhaustOnOffList.append(Exhaust_On_Off_s)
        PressureList.append(PressureValue_s)
        pHValueList.append(pHValue_s)
        SetPoint1List.append(2)
        SetPoint2List.append(8)

        # print(current_time)
        #print("Running in update_data_log Timer")
        
        # rows = [x[i], y[i]]
        rows = [x[i], x_time[i], TopTemperatureList[i], BottomTemperatureList[i], y[i],
                HeartTemperatureList[i], DryIceList[i], BlowerPIDOutputList[i], BlowerPWMOutputList[i],
                BlowerOnOffList[i], ExhaustOnOffList[i], PressureList[i], pHValueList[i]]
        # # writing to csv file
        with open(filename, 'a', newline='') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile, delimiter=",")

            # writing the data rows
            csvwriter.writerow(rows)
            csvfile.close()

        TriggerDataLog = False
        TriggerPlotting = False
        time.sleep(0.1)

    def update_data_plot(self):
        global AverageTemperature  # Use global variable AverageTemperature
        global TopTemperature  # Use global variable TopTemperature
        global BottomTemperature  # Use global variable BottomTemperature
        global HeartTemperature  # Use global variable HeartTemperature
        global DryIce  # Use global variable DryIce
        global BlowerPWM  # Use global variable BlowerPWM
        global TopTemperatureList
        global BottomTemperatureList
        global HeartTemperatureList
        global DryIceList
        global BlowerPIDOutputList
        global BlowerPWMOutputList
        global SetPoint1List
        global SetPoint2List
        global x
        global x_time
        global y
        global i
        global TriggerPlotting
        global Time_i

        # self.plot(x, y, 'g')
        # self.plot(x, SetPoint1List, 'r')
        # self.plot(x, SetPoint2List, 'r')
        # self.plot(x, TopTemperatureList, 'y')
        # self.plot(x, BottomTemperatureList, 'c')
        # self.plot(x, HeartTemperatureList, 'm')


class UpdateThread(QThread):

    def __init__(self,*args):
        #QThread.__init__(self)
        super().__init__()
    def run(self):
        global GUIOBJECT  # Use global variable GUIOBJECT
        global AverageTemperature  # Use global variable AverageTemperature
        global TopTemperature  # Use global variable TopTemperature
        global BottomTemperature  # Use global variable BottomTemperature
        global HeartTemperature  # Use global variable HeartTemperature
        global DryIce  # Use global variable DryIce
        global BlowerPWM  # Use global variable BlowerPWM
        global Feedback
        global SERIALOBJECT  # Use global variable SERIALOBJECT
        global ConnectRequest
        global CoolingONRequest
        global CoolingOFFRequest
        global PerfusionONRequest
        global PerfusionOFFRequest
        global DryIceTareRequest
        global PerfusionFluidTareRequest
        global WasteFluidTareRequest
        global UpdatePerfusionSettingsRequest
        global index1
        global index2
        global index3
        global otf
        global ExhaustONRequest
        global ExhaustOFFRequest
        global TopTemperature_s
        global TopTemperature_f
        global BottomTemperature_s
        global BottomTemperature_f
        global AverageTemperature_s
        global AverageTemperature_f
        global HeartTemperature_s
        global HeartTemperature_f
        global DryIceLoad_s
        global DryIceLoad_f
        global SalineOneLoad_s
        global SalineOneLoad_f
        global SalineTwoLoad_s
        global SalineTwoLoad_f
        global BlowerPWM_s
        global BlowerPWM_f
        global BlowerPIDOutput_s
        global BlowerPIDOutput_f
        global Blower_On_Off_s
        global Blower_On_Off_f
        global Exhaust_On_Off_s
        global Exhaust_On_Off_f
        global i
        global FlowRate
        global TimeInterval
        global ReqPerfusionData_s
        global ReqPerfusionTime_s
        global PumpOneStatus_s
        global PumpTwoStatus_s
        global GsecCounter_s
        global GsecCounter_f
        global SecondCount_s
        global SecondCount_f
        global PressureValue_s
        global PressureValue_f
        global pHValue_s
        global pHValue_f
        global Motor1ForwardOFFRequest
        global Motor1ForwardONRequest
        global Motor2ForwardOFFRequest
        global Motor2ForwardONRequest
        global Motor1BackwardOFFRequest
        global Motor1BackwardONRequest
        global Motor2BackwardOFFRequest
        global Motor2BackwardONRequest
        global ResetPerfusionDataRequest
        global NumOfPerfusionCycles_s
        global NumOfPerfusionCycles_f
        global patchFlag
        # ser = serial.Serial('com4', baudrate=9600, timeout=100)  # open serial port
        # ser = serial.Serial('com13', baudrate=115200, timeout=10000)  # open serial port in PC
        ser = serial.Serial(port='/dev/ttyS0', baudrate=115200, timeout=1000)  # open serial port in Raspberry Pi
        # print(ser.is_open)  # Print and check if the port is open
        # print(ser.name)    # Print the name of the port
        
                
        while 1:  # For always
            #QtWidgets.QApplication.processEvents()
            if ConnectRequest == 1:
                ser.flush()
                ser.reset_output_buffer()
                ser.write(b'1')
                ConnectRequest = 0
                ser.reset_input_buffer()
                time.sleep(0.1)
                Feedback = ser.readline().decode('ascii')
                print(Feedback)
            elif ConnectRequest == 2:
                ser.flush()
                ser.reset_output_buffer()
                ser.write(b'2')
                ConnectRequest = 0
                ser.reset_input_buffer()
                Feedback = ser.readline().decode('ascii')
                time.sleep(0.01)
                print(Feedback)

            if Feedback == 'A\n':  # STM
                # if Feedback == 'A\r\n':  # Arduino
                # ser.reset_input_buffer()
                try:
                    if patchFlag==1:
                        #ser.reset_output_buffer()
                        #ser.reset_input_buffer()
                        #ser.flush()
                        #ser.write(b'Z')
                        GUIOBJECT.dummyButton.click()
                        GUIOBJECT.dummyButton.setVisible(True)
                        GUIOBJECT.dummyButton.setVisible(False)
                        patchFlag=0
                        print("Patched")
            
                    chkStart = ser.readline().decode('ascii')
                    
                    if "***" in chkStart:
                        TopTemperature_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, TopTemperature_s))
                        TopTemperature_s = TopTemperature_s.strip('\r\n')
                        TopTemperature_s = TopTemperature_s.strip('\x00')
                        # print(TopTemperature_s)
                        # time.sleep(0.1)
                        # ser.reset_input_buffer()
                        BottomTemperature_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, BottomTemperature_s))
                        BottomTemperature_s = BottomTemperature_s.strip('\r\n')
                        BottomTemperature_s = BottomTemperature_s.strip('\x00')
                        
                        # print(BottomTemperature_s)
                        # time.sleep(0.1)
                        # ser.reset_input_buffer()
                        AverageTemperature_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, AverageTemperature_s))
                        AverageTemperature_s = AverageTemperature_s.strip('\r\n')
                        AverageTemperature_s = AverageTemperature_s.strip('\x00')
                        # print(AverageTemperature_s)
                        # time.sleep(0.1)
                        # ser.reset_input_buffer()
                        HeartTemperature_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, HeartTemperature_s))
                        HeartTemperature_s = HeartTemperature_s.strip('\r\n')
                        HeartTemperature_s = HeartTemperature_s.strip('\x00')
                        # print(HeartTemperature_s)
                        # time.sleep(0.1)
                        # ser.reset_input_buffer()
                        DryIceLoad_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, DryIceLoad_s))
                        DryIceLoad_s = DryIceLoad_s.strip('\r\n')
                        DryIceLoad_s = DryIceLoad_s.strip('\x00')
                        # print(DryIceLoad_s)
                        # time.sleep(0.1)
                        # ser.reset_input_buffer()
                        SalineOneLoad_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, SalineOneLoad_s))
                        SalineOneLoad_s = SalineOneLoad_s.strip('\r\n')
                        SalineOneLoad_s = SalineOneLoad_s.strip('\x00')

                        SalineTwoLoad_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, SalineTwoLoad_s))
                        SalineTwoLoad_s = SalineTwoLoad_s.strip('\r\n')
                        SalineTwoLoad_s = SalineTwoLoad_s.strip('\x00')

                        BlowerPIDOutput_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, BlowerPIDOutput_s))
                        BlowerPIDOutput_s = BlowerPIDOutput_s.strip('\r\n')
                        BlowerPIDOutput_s = BlowerPIDOutput_s.strip('\x00')

                        BlowerPWM_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, BlowerPWM_s))                
                        BlowerPWM_s = BlowerPWM_s.strip('\r\n')
                        BlowerPWM_s = BlowerPWM_s.strip('\x00')

                        Blower_On_Off_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, Blower_On_Off_s))                
                        Blower_On_Off_s = Blower_On_Off_s.strip('\r\n')
                        Blower_On_Off_s = Blower_On_Off_s.strip('\x00')

                        Exhaust_On_Off_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, Exhaust_On_Off_s))
                        Exhaust_On_Off_s = Exhaust_On_Off_s.strip('\r\n')
                        Exhaust_On_Off_s = Exhaust_On_Off_s.strip('\x00')

                        ReqPerfusionData_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, ReqPerfusionData_s))
                        ReqPerfusionData_s = ReqPerfusionData_s.strip('\r\n')
                        ReqPerfusionData_s = ReqPerfusionData_s.strip('\x00')

                        ReqPerfusionTime_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, ReqPerfusionTime_s))
                        ReqPerfusionTime_s = ReqPerfusionTime_s.strip('\r\n')
                        ReqPerfusionTime_s = ReqPerfusionTime_s.strip('\x00')

                        GsecCounter_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, GsecCounter_s))
                        GsecCounter_s = GsecCounter_s.strip('\r\n')
                        GsecCounter_s = GsecCounter_s.strip('\x00')

                        SecondCount_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, SecondCount_s))
                        SecondCount_s = SecondCount_s.strip('\r\n')
                        SecondCount_s = SecondCount_s.strip('\x00')
                        
                        PumpOneStatus_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, PumpOneStatus_s))
                        PumpOneStatus_s = PumpOneStatus_s.strip('\r\n')
                        PumpOneStatus_s = PumpOneStatus_s.strip('\x00')

                        PumpTwoStatus_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, PumpTwoStatus_s))
                        PumpTwoStatus_s = PumpTwoStatus_s.strip('\r\n')
                        PumpTwoStatus_s = PumpTwoStatus_s.strip('\x00')

                        PressureValue_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, PressureValue_s))
                        PressureValue_s = PressureValue_s.strip('\r\n')
                        PressureValue_s = PressureValue_s.strip('\x00')

                        pHValue_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, pHValue_s))
                        pHValue_s = pHValue_s.strip('\r\n')
                        pHValue_s = pHValue_s.strip('\x00')

                        NumOfPerfusionCycles_s = ser.readline().decode('ascii')  # Read the line on serial port
                        ''.join(filter(str.isdigit, NumOfPerfusionCycles_s))
                        NumOfPerfusionCycles_s = NumOfPerfusionCycles_s.strip('\r\n')
                        NumOfPerfusionCycles_s = NumOfPerfusionCycles_s.strip('\x00')


                        TopTemperature_f = float(TopTemperature_s)  # copy the Top temperature value for Plotting and Logging
                        BottomTemperature_f = float(BottomTemperature_s)  # copy the Bottom temperature value for Plotting and Logging
                        AverageTemperature_f = float(AverageTemperature_s)  # copy the Average temperature value for Plotting and Logging
                        HeartTemperature_f = float(HeartTemperature_s)  # copy the heart temperature value for Plotting and Logging
                        DryIceLoad_f = float(DryIceLoad_s)  # copy the DryIce Units value for Plotting and Logging
                        SalineOneLoad_f = float(SalineOneLoad_s)  # copy the DryIce Units value for Plotting and Logging
                        SalineTwoLoad_f = float(SalineTwoLoad_s)  # copy the DryIce Units value for Plotting and Logging
                        BlowerPIDOutput_f = float(BlowerPIDOutput_s)  #
                        BlowerPWM_f = float(BlowerPWM_s)  #
                        Blower_On_Off_f = float(Blower_On_Off_s)  #
                        Exhaust_On_Off_f = float(Exhaust_On_Off_s)  #
                        GsecCounter_f = float(GsecCounter_s)  #
                        SecondCount_f = float(SecondCount_s)  #
                        PressureValue_f = float(PressureValue_s)  #
                        pHValue_f = float(pHValue_s)  #
                        NumOfPerfusionCycles_f = float(NumOfPerfusionCycles_s)  #
                    else:
                        print("Not synced")
                        ser.reset_input_buffer()
                
                except Exception as e: print(e)
                    

                # try:  # Manages exceptions

                GUIOBJECT.Count1lcdNum.display(TopTemperature_f)  # Display the count on lcd display
                GUIOBJECT.Count2lcdNum.display(BottomTemperature_f)  # Display the count on lcd display
                GUIOBJECT.Count3lcdNum.display(AverageTemperature_f)  # Display the count on lcd display
                GUIOBJECT.Count4lcdNum.display(HeartTemperature_f)  # Display the count on lcd display
                GUIOBJECT.Count5lcdNum.display(DryIceLoad_f )  # Display the count on lcd display
                GUIOBJECT.Count5lcdNum_2.display(SalineOneLoad_f)  # Display the count on lcd display
                GUIOBJECT.Count5lcdNum_3.display(SalineTwoLoad_f)  # Display the count on lcd display
                #GUIOBJECT.Count5lcdNum_4.display(8888)
                #GUIOBJECT.Count5lcdNum_5.display(8888)
                GUIOBJECT.testLabel.setVisible(True) 
                GUIOBJECT.testLabel.setText(GsecCounter_s)
                GUIOBJECT.testLabel.setVisible(False)
                GUIOBJECT.Count5lcdNum_4.display(GsecCounter_f)  # Display the count on lcd display
                time.sleep(0.1)
                GUIOBJECT.PressureLCD.display(PressureValue_f)  # Display the count on lcd display
                GUIOBJECT.pHLCD.display(pHValue_f)  # Display the count on lcd display
                GUIOBJECT.Count5lcdNum_5.display((TimeInterval) - SecondCount_f)        
                GUIOBJECT.Count5lcdNum_6.display(NumOfPerfusionCycles_f)
                print((TimeInterval) - SecondCount_f)
                # GUIOBJECT.pwmLabel.setNum(BlowerPWM_f)
                # print("No Error")
                # except ValueError:
                # print("Value Error")  # Print error
                if PumpOneStatus_s == '1':
                    #GUIOBJECT.gif.start()
                    GUIOBJECT.label_8.setText("Motor 1 ON")
                else:
                    GUIOBJECT.label_8.setText("Motor 1 OFF")
                if PumpTwoStatus_s == '1':
                    #GUIOBJECT.gif.start()
                    GUIOBJECT.label_9.setText("Motor 2 ON")
                else:
                    GUIOBJECT.label_9.setText("Motor 2 OFF")
                if CoolingONRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'C')
                    CoolingONRequest = 0
                elif CoolingOFFRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'c')
                    CoolingOFFRequest = 0
                elif DryIceTareRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'T')
                    DryIceTareRequest = 0
                elif ExhaustONRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'X')
                    ExhaustONRequest = 0
                elif ExhaustOFFRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'x')
                    ExhaustOFFRequest = 0
                elif PerfusionFluidTareRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'L')
                    PerfusionFluidTareRequest = 0
                elif WasteFluidTareRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'l')
                    WasteFluidTareRequest = 0
                elif UpdatePerfusionSettingsRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'U')
                    UpdatePerfusionSettingsRequest = 0
                elif ReqPerfusionTime_s == '1':
                    ser.reset_output_buffer()
                    ser.write(b'%d' % index3)
                    print("printing in serial write ReqPerfusionTime_s = 1")
                    GUIOBJECT.StartStopPerfusionButton.setEnabled(True)
                    GUIOBJECT.StartStopPerfusionButton.setStyleSheet("background-color: green; color: white\n"+
                                                                "border-radius: 5px; border: 2px groove gray;\n"+
                                                                "border-style: outset;")
                elif ReqPerfusionData_s == '1':
                    if otf == 1:
                        ser.reset_output_buffer()
                        #numOfBytesWritten = ser.write(b'%d' % index1 + b'%d' % index2)
                        ser.write(b'%d' % index1)
                        #time.sleep(0.01)
                        print("printing in serial write ReqPerfusionData_s = 1")
                        print("index1 FlowRateCB = ", index1)
                        print("index2 IntervalCB = ", index2)
                        print("index3 PerfusionTimeCB = ", index3)
                        #print("numOfBytesWritten = ",numOfBytesWritten)
                        otf = 2
                    #ReqPerfusionData_s = '0'
                    elif otf == 2:
                        ser.write(b'%d' % index2)
                        otf = 3
                elif PerfusionONRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'P')
                    PerfusionONRequest = 0
                elif PerfusionOFFRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'p')
                    PerfusionOFFRequest = 0
                elif Motor1ForwardONRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'M')#M is main pump
                    Motor1ForwardONRequest = 0
                elif Motor1ForwardOFFRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'm')
                    Motor1ForwardOFFRequest = 0
                elif Motor2ForwardONRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'S')#S is secondary pump
                    Motor2ForwardONRequest = 0
                elif Motor2ForwardOFFRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b's')
                    Motor2ForwardOFFRequest = 0
                elif Motor1BackwardONRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'F')#M is main pump
                    Motor1BackwardONRequest = 0
                elif Motor1BackwardOFFRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'f')
                    Motor1BackwardOFFRequest = 0
                elif Motor2BackwardONRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'R')#S is secondary pump
                    Motor2BackwardONRequest = 0
                elif Motor2BackwardOFFRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'r')
                    Motor2BackwardOFFRequest = 0.
                elif ResetPerfusionDataRequest == 1:
                    ser.reset_output_buffer()
                    ser.write(b'I')
                    ResetPerfusionDataRequest = 0                
            #print("Running in while loop of update thread")
            time.sleep(0.1)
        #print("Running in update Thread")

class PlottingThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global AverageTemperature  # Use global variable AverageTemperature
        global TopTemperature  # Use global variable TopTemperature
        global BottomTemperature  # Use global variable BottomTemperature
        global HeartTemperature  # Use global variable HeartTemperature
        global DryIce  # Use global variable DryIce
        global BlowerPWM  # Use global variable BlowerPWM
        global TopTemperatureList
        global BottomTemperatureList
        global HeartTemperatureList
        global DryIceList
        global BlowerPIDOutputList
        global BlowerPWMOutputList
        global SetPoint1List
        global SetPoint2List
        global x
        global x_time
        global y
        global i
        global TriggerPlotting
        global TriggerDataLog
        global TopTemperature_s
        global TopTemperature_f
        global BottomTemperature_s
        global BottomTemperature_f
        global AverageTemperature_s
        global AverageTemperature_f
        global HeartTemperature_s
        global HeartTemperature_f
        global DryIceLoad_s
        global DryIceLoad_f
        global BlowerPWM_s
        global BlowerPWM_f
        global rows

        # while 1:
        # while TriggerPlotting:
        # self.PlotData()
        # if ConnectRequest == 2:
        #     ex = pg.exporters.ImageExporter(GUIOBJECT.graphicsView.scene())
        #     ex.export("TemperaturePlot.png")

    # def PlotData(self):
    # GUIOBJECT.plot(x, y, 'g')
    # GUIOBJECT.plot(x, SetPoint1List, 'r')
    # GUIOBJECT.plot(x, SetPoint2List, 'r')
    # GUIOBJECT.plot(x, TopTemperatureList, 'y')
    # GUIOBJECT.plot(x, BottomTemperatureList, 'c')
    # GUIOBJECT.plot(x, HeartTemperatureList, 'm')


class MainGUIThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global SERIALOBJECT  # Use global variable SERIALOBJECT
        global GUIOBJECT  # Use global variable GUIOBJECT
        global Plotting_Thread
        app = QtWidgets.QApplication(sys.argv)  # Create an app
        MainWindow = QtWidgets.QMainWindow()  # Create the main window
        GUIOBJECT = Ui_MyGUI()  # Create a GUI object
        GUIOBJECT.setupUi(MainWindow)  # Setup the main window in my Gui object
        Update_Thread = UpdateThread()  # Create the thread Update.
        Update_Thread.start()  # Start the thread Update.
        # Plotting_Thread = PlottingThread()  # Create the thread Plotting.
        # Plotting_Thread.start()  # Start the thread Update.
        #MainWindow.show()  # Display the main window.
        MainWindow.showFullScreen()
        #QtWidgets.QApplication.processEvents()
        sys.exit(app.exec_())  # Exit the program when the main windows is closed.


if __name__ == "__main__":
    import sys

    #mainThread = MainGUIThread()  # Create the main thread for the GUI
    #mainThread.start()  # Start the thread for the GUI
    #global SERIALOBJECT  # Use global variable SERIALOBJECT
    #global GUIOBJECT  # Use global variable GUIOBJECT
    #global Plotting_Thread
    app = QtWidgets.QApplication(sys.argv)  # Create an app
    MainWindow = QtWidgets.QMainWindow()  # Create the main window
    GUIOBJECT = Ui_MyGUI()  # Create a GUI object
    GUIOBJECT.setupUi(MainWindow)  # Setup the main window in my Gui object
    Update_Thread = UpdateThread()  # Create the thread Update.
    Update_Thread.start()  # Start the thread Update.
    sys.setswitchinterval(0.001)
    # Plotting_Thread = PlottingThread()  # Create the thread Plotting.
    # Plotting_Thread.start()  # Start the thread Update.
    #MainWindow.show()  # Display the main window.
    MainWindow.showFullScreen()
    #QtWidgets.QApplication.processEvents()
    sys.exit(app.exec())  # Exit the program when the main windows is closed.
