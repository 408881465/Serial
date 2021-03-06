from PyQt5 import uic
from PyQt5.QtChart import QChartView
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QDir
from Serial import Serial

class Ui(QMainWindow):
    def __init__(self, executable_path):
        super(Ui, self).__init__()
        ui_file = executable_path + QDir.separator() + 'Serial.ui'
        uic.loadUi(ui_file, self)
        self.serial = Serial()
        self.__signals()
        self.show()
    
    def __signals(self):
        self.page_forward_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))
        self.page_backward_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page))

        # choose baudrate -> change the baud rate in Serial
        self.baudrate_combobox.currentTextChanged.connect( self.serial.setBaudRate_str )
        # choose port -> fire slot on_new_portName
        self.ports_combobox.currentItemChanged.connect(self.serial.on_new_portName)
        # choose a new port -> reset Chart
        self.ports_combobox.currentItemChanged.connect(self.graphicsView.reset)
        # choose a new port -> clear serial out
        self.ports_combobox.currentItemChanged.connect(self.serial_out.reset)
        # serial have something to read -> append reading to serial_out
        self.serial.readyRead[str].connect(self.serial_out.on_serial_read)
        # there is data to be read -> draw it
        self.serial.readyRead[int].connect(self.graphicsView.draw_point)
        # resource becomes unavailable -> reset ports_combobox
        self.serial.resourcesUnavailable.connect(self.ports_combobox.reset)
        # user write data -> sent it
        self.serial_input.serial_input_sent.connect(self.serial.write_line_read)
