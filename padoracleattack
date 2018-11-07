from paddingoracle import BadPaddingException, PaddingOracle
from base64 import b64encode, b64decode
from urllib import quote, unquote
import requests
import socket
import time
 
 
RHOST = '10.10.10.89'
RPORT = 1550
BUFFER_SIZE = 128
 
class PadBuster(PaddingOracle):
    def __init__(self, **kwargs):
        super(PadBuster, self).__init__(**kwargs)
        self.session = requests.Session()
        self.wait = kwargs.get('wait', 2.0)
 
    def oracle(self, data, **kwargs):
        #somecookie = quote(b64encode(data))
        somecookie = b64encode(data)
        print 'Data : ',somecookie
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((RHOST, RPORT))
        data = ""
        while 'Insert ciphertext: ' not in data:
            data = s.recv(BUFFER_SIZE) # first line
            print 'Data : ',data
        a = s.send(somecookie+'\n')
        print 'Sent : ',a
        answer = s.recv(BUFFER_SIZE)
        print 'Received : ', answer
 
        if 'Invalid Padding!'  not in answer:
            logging.debug('No padding exception raised on %r', somecookie)
            return
 
        raise BadPaddingException
 
 
if __name__ == '__main__':
    import logging
    import sys
 
    if not sys.argv[1:]:
        print 'Usage: %s <somecookie value>' % (sys.argv[0], )
        sys.exit(1)
 
    logging.basicConfig(level=logging.DEBUG)
 
    encrypted_cookie = b64decode(unquote(sys.argv[1]))
    print 'Base64 decrypted',encrypted_cookie
    padbuster = PadBuster()
 
    cookie = padbuster.decrypt(encrypted_cookie, block_size=16, iv=bytearray(8))
 
    print('Decrypted somecookie: %s => %r' % (sys.argv[1], cookie))
