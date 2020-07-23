import socket

class ServerSocket :

    def __init__(self, IP = "0.0.0.0", Port = 12345):

        self.Server = socket.socket()
        self.Server.bind((IP, Port))
        self.Server.listen(1)
        self.Client, Adder = self.Server.accept()
        print("Client with adder : " + str(Adder) + " Connected !!!\n")

    def Socket (self) :
        return self.Client

    def __del__(self):
        self.Server.close()
        self.Client.close()


class ClientSocket :

    def __init__(self, IP = "localhost", Port = 12345):
        self.Client = socket.socket()
        self.Client.connect((IP, Port))

    def Socket(self):
        return self.Client

    def __del__(self):
        self.Client.close()
