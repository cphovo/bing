import os
import binascii

def generate_api_token():
    return 'cphovo-' + binascii.hexlify(os.urandom(20)).decode()

token = generate_api_token()
print(token)
