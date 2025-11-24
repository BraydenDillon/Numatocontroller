import serial 
import numpy as np
class write32:
    def __init__(self, portname):
        self.portname = portname

    def on_off(self, relaynum, relaycmd):
        serport = serial.Serial(str(self.portname), 9600, 8)
        Alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V']
        if relaynum > 9:
            new_relaynum = Alphabet[relaynum - 10]

        else:
            new_relaynum = relaynum

        serport.write(str.encode('relay '+str(relaycmd)+' '+str(new_relaynum)+ '\n\r'))

    def _del_(self):
        try:
            self.on_off()
        except:
            pass
