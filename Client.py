from Socket import ClientSocket
from SessionKeyExchange import ClientSession
from Cryptography import session_crypto

KEY_THRESHOLD = 2

def __main__():
    # Create connection socket
    connection = ClientSocket()
    sock = connection.Socket()

    # Key exchange class for session key generation
    key_exchange = ClientSession(sock)
    session_key = key_exchange.new_session()
    crypto_system = session_crypto(session_key)

    print("Successfully connecetd to the server.")
    
    fresh_key = 0
    while True:
        print('session key: ', crypto_system.key)
        command = input('Enter your command > ').strip()
        
        # Encrypt and entered send command
        enc_command = crypto_system.encrypt(command)
        sock.send(enc_command)

        '''
        response = crypto_system.decrypt(sock.recv(4096))
        '''

        # Increase session key lifetime and generate
        # a new one if needed at the end of this loop 
        fresh_key += 1
        if (fresh_key > KEY_THRESHOLD):
            fresh_key = 0
            session_key = key_exchange.key_freshness()
            crypto_system.key = session_key

        


__main__()
