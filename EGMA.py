#dev. xspider 
import base64
import sys, socket, select
from Crypto.Cipher import AES
import os
import hashlib
import signal

os.system("clear")
print """
	
   ++++++++++++++++++++++++++++++++++++++++++++
   +##########################################+
   +#        welcome to EGMA massenger       #+
   +##########################################+
   ++++++++++++++++++++++++++++++++++++++++++++
   dev. : xspider

"""

def sigint_handler(signum, frame):
    print '\n[-] user interrupt ! shutting down[-]'
    print "[info] shutting down EGMA massenger \n\n"
    sys.exit()	
    

signal.signal(signal.SIGINT, sigint_handler)

def hasher(key):
	hash_object = hashlib.sha512(key)
	hexd = hash_object.hexdigest()
	hash_object = hashlib.md5(hexd)
	hex_dig = hash_object.hexdigest()
	return hex_dig

def encrypt(secret,data):
	BLOCK_SIZE = 32
	PADDING = '{'
	pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
	EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
	cipher = AES.new(secret)
	encoded = EncodeAES(cipher, data)
	return encoded

def decrypt(secret,data):
	BLOCK_SIZE = 32
	PADDING = '{'
	pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
	DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
	cipher = AES.new(secret)
	decoded = DecodeAES(cipher, data)
	return decoded


def chat_client():
    if(len(sys.argv) < 5) :
        print 'Usage : python EGMA.py <hostname> <port> <password> <nick_name>'
        print 'Example :: python EGMA.py 172.0.0.1 5329 pass124 ali'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    key = sys.argv[3]
    key = hasher(key)	
    uname = sys.argv[4]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)


    try :
        s.connect((host, port))

    except :
        os.system("bash error.sh")
        sys.exit()
    os.system("bash con.sh")
    sys.stdout.write("\033[34m"+'\n[Me :] '+ "\033[0m"); sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            if sock == s:

                data = sock.recv(4096)

                if not data :
                    print "\033[91m"+"\nDisconnected from chat room server"+"\033[0m"
                    sys.exit()
                else :
                    data = decrypt(key,data)
                    sys.stdout.write(data)
                    sys.stdout.write("\033[34m"+'\n[Me :] '+ "\033[0m"); sys.stdout.flush()

            else :

                msg = sys.stdin.readline()
                msg = '[ '+ uname +': ] '+msg
                msg = encrypt(key,msg)
                s.send(msg)
                sys.stdout.write("\033[34m"+'\n[Me :] '+ "\033[0m"); sys.stdout.flush()

if __name__ == "__main__":

    sys.exit(chat_client())
