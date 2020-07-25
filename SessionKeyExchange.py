import random
from datetime import datetime
import hashlib

# 2048-bit Prime
PRIME = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
GENERATOR = 2

class ClientSession():
    def __init__(self, sock):
        self.session_key = 0
        self.counter = 0
        self.sock = sock

    def new_session(self):
        # Generate public/private keypair
        public_key, private_key = _generate_keypair()

        # Public key exchange
        server_pub_key = int(self.sock.recv(2048).decode())
        self.sock.send(str(public_key).encode())

        self.session_key = pow(server_pub_key, private_key, PRIME)
        return _gen_aes_key(self.counter, self.session_key)

    def key_freshness(self):
        self.counter += 1
        return _gen_aes_key(self.counter, self.session_key)
        


class ServerSession():
    def __init__(self, sock):
        self.session_key = 0
        self.counter = 0
        self.sock = sock

    def new_session(self):
        # Generate public/private keypair
        public_key, private_key = _generate_keypair()
   
        # Public key exchange
        self.sock.send(str(public_key).encode())
        client_pub_key = int(self.sock.recv(2048).decode())
        
        self.session_key = pow(client_pub_key, private_key, PRIME)
        return _gen_aes_key(self.counter, self.session_key)

    def key_freshness(self):
        self.counter += 1
        return _gen_aes_key(self.counter, self.session_key)

def _generate_keypair():
        random.seed(datetime.now())
        private_key = random.randint(2, PRIME - 2)
        public_key = pow(GENERATOR, private_key, PRIME)
        return public_key, private_key

def _gen_aes_key(counter, session_key):
    H = hashlib.new('sha256')
    H.update(hex(counter + session_key).encode('ascii'))
    b_hash = H.digest()
    return b_hash