import base64
import binascii
from uuid import getnode
import socket


class Computer:
    def get_hwid(self):
        # TODO: find more unique things to use in HWID
        hwid = '{0}'.format(self.get_mac()).encode('utf-8')
        b64 = base64.b64encode(hwid)
        return binascii.hexlify(b64).upper().decode('utf-8')
    
    def get_mac(self):
        return getnode()
    
    def get_hostname(self):
        return socket.gethostname()
