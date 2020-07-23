import hashlib
from Crypto.Cipher import AES
from Crypto.Util import Padding
from Crypto.Random import get_random_bytes

class session_crypto:
    def __init__(self, key):
        self.key = key

    def encrypt(self, msg):
        if isinstance(msg, bytes):
            msg = msg.decode()
        IV = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CFB, iv=IV)
        hashed_msg = self.sha256(msg.encode('ascii'))
        encMsg = cipher.encrypt(msg.encode())
        return encMsg + hashed_msg + IV


    def decrypt(self, msg):
        IV = msg[len(msg)-16: ]
        expected_hash = msg[len(msg)-48 : len(msg)-16]
        msg = msg[ : len(msg)-48]
        cipher = AES.new(self.key, AES.MODE_CFB,  iv=IV)
        decMsg = cipher.decrypt(msg).decode('utf-8')
        hashed_msg = self.sha256(decMsg.encode('ascii'))
        if (hashed_msg != expected_hash):
            return -1
        else:
            return decMsg

    def sha256(self, msg):
        if not isinstance(msg, bytes):
            msg = msg.encode('ascii')
        H = hashlib.new('sha256')
        H.update(msg)
        b_hash = H.digest()
        return b_hash
