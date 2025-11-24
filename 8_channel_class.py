import serial 
import numpy as np
import time
import sys
class relaywrite:
    def __init__(self, portname):
        self.portname = portname
        self._status = np.array(['0','0','0','0','0','0','0','0'])

    def get_status(self):
        with serial.Serial(str(self.portname), 9600, 8) as serport:
            serport.write(b'relay readall\n\r')
            #serport.reset_input_buffer()
            #serport.reset_output_buffer()
            time.sleep(0.0001)
            hexa = serport.read_all().decode(errors = 'ignore')[16:18]

            dec = int(hexa, 16)
            return f'{dec:08b}'
        

    def on_off(self, relaynum, relaycmd):
        try: 
            with serial.Serial(str(self.portname), 9600, 8) as serport:
        
                serport.write(str.encode('relay '+str(relaycmd)+' '+str(relaynum)+ '\n\r'))
        
            print('Command Sent')
        
            if relaycmd == 'on':
                self._status[relaynum] = '1'
            elif relaynum =='off':
                self._status[relaynum] = '0'
        
        except serial.SerialException as e:
            print(f'Error opening or communicating with serial port: {e}')
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
   
    def status_to_hex(self, lst):
        binary = ''.join(lst)
        dec = int(binary, 2)
        return f'{dec:02x}'
    
    def simul(self, lower, upper, cmd):
        '''
        Can specify arrangement of on/off relays via indexing
        '''
        #print(self._status[::-1])
        try:

            if cmd == 'on':
                self._status[lower:upper+1] = 1
            elif cmd == 'off':
                self._status[lower:upper+1] = 0
            relaycmd = self.status_to_hex(self._status[::-1])
            #print(self._status[::-1])
        # write intended state, then query relay state. If they don't match throw error
            with serial.Serial(str(self.portname), 9600, timeout = 1) as serport:
                serport.write(str.encode('relay writeall ' + str(relaycmd)+'\n\r'))

            relaystat = self.get_status()
            if relaystat != ''.join(self._status[::-1]):
                print('Error: status is inconsistent with relay')
                sys.exit(1)
                    

        except serial.SerialException as e:
            print(f'Error opening or communicating with serial port: {e}')
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
    
    
        
    def kill(self):
        try:
            with serial.Serial(str(self.portname), 9600, timeout = 1) as serport:
                serport.write(str.encode('relay writeall 00\n\r'))

        except serial.SerialException as e:
            print(f'Error opening or communicating with serial port: {e}')
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    

    def _del_(self):
        try:
            self.on_off()
        except:
            pass
        try:
            self.get_status()
        except:
            pass
        try:
            self.status_to_hex()
        except:
            pass
        try:
            self.simul()
        except:
            pass
        try:
            self.kill()
        except:
            pass
        
