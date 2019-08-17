import config
import serial

class OutputToSerial(object):
    def __init__(self):
        self.serial_1 = config.OUT_COM_PORT_1
        self.serial_2 = config.OUT_COM_PORT_2
        self.serial_3 = config.OUT_COM_PORT_3
        self.serial_4 = config.OUT_COM_PORT_4
    
    def redirectSTDOUtoSerial_1(self, data=None):
        with serial.Serial(self.serial_1) as com1:
            com1.write(data)
    
    def redirectSTDOUtoSerial_2(self, data=None):
        with serial.Serial(self.serial_2) as com2:
            com2.write(data)

    def redirectSTDOUtoSerial_3(self, data=None):
        with serial.Serial(self.serial_3) as com3:
            com3.write(data)

    def redirectSTDOUtoSerial_4(self, data=None):
        with serial.Serial(self.serial_4) as com4:
            com4.write(data)
    
    def manageOut(self, comID, data=None):
        if type(comID) == int:
            if comID == 0:
                pass
            elif comID == 1:
                self.redirectSTDOUtoSerial_1(data)
            elif comID == 2:
                self.redirectSTDOUtoSerial_2(data)
            elif comID == 3:
                self.redirectSTDOUtoSerial_3(data)
            elif comID == 4:
                self.redirectSTDOUtoSerial_4(data)
 
    def recordVideoOut(self):
        pass

if __name__ == '__main__':
    OUT_TO_COM = OutputToSerial()
    WRITE_TO_COM_1 = OUT_TO_COM.redirectSTDOUtoSerial_1('test data')
    WRITE_TO_COM_2 = OUT_TO_COM.redirectSTDOUtoSerial_2('test data')
    WRITE_TO_COM_3 = OUT_TO_COM.redirectSTDOUtoSerial_3('test data')
    WRITE_TO_COM_4 = OUT_TO_COM.redirectSTDOUtoSerial_4('test data')
