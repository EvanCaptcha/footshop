from computer import Computer
from encryption import decrypt
import os

license_file = 'license.key'

def read_license():
    try:
        with open(license_file, 'r') as f:
            return f.read()
    except:
        return None

def verify_license(key):
    computer = Computer()
    return decrypt(key) == computer.get_hwid()

def write_license(key):
    if not os.path.exists(license_file):
        with open(license_file, 'w') as f:
            f.write(key)
