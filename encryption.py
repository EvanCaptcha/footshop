import pyaes
import base64

key = 'cfb5VTTC6naPFOjoneSiOEsZYbdKfUQd'.encode('utf-8')


def encrypt(msg):
    aes = pyaes.AESModeOfOperationCTR(key)
    return base64.b64encode(aes.encrypt(msg)).decode('utf-8')

def decrypt(msg):
    try:
        msg = base64.b64decode(msg)
        aes = pyaes.AESModeOfOperationCTR(key)
        return aes.decrypt(msg).decode('utf-8')
    except:
        return None
