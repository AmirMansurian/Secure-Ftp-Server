import re
import Socket
import Cryptography
import Registery
import  Login
import Download
import Upload



class Server :

    def __init__(self, Socket, Crypto, Register, Login, Download, Upload):

        self.Socket = Socket
        self.Crypto = Crypto
        self.Register = Register
        self.Login = Login
        self.Upload = Upload
        self.Download = Download


    def Handler (self) :

        while 1 :

            Encrypted = self.Socket.recv(2048)
            Command = self.Crypto.decrypt(Encrypted)

            if Command == -1 :
                self.Socket.sendall(self.Crypto.encrypt("Please try again !!!\n"))

            else :

                Sets = Command.split(" ")

                if re.match(r'register', Sets[0], re.I) != None :

                    if len(Sets) != 5 :
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else :
                        Response = self.Register.Registeration(Sets[1:], self.Crypto)
                        self.Socket.sendall(self.Crypto.encrypt(Response + "\n"))

                elif re.match(r'login', Sets[0], re.I) != None :

                    if len(Sets) != 3 :
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else :
                        Response = self.Login.Login(Sets[1], Sets[2], self.Crypto)
                        self.Socket.sendall(self.Crypto.encrypt(Response + "\n"))

                elif re.match(r'put', Sets[0], re.I) != None :

                    if len(Sets) != 4 :
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else :
                        Response = self.Upload.PutFile(Sets[1:], "ali")
                        self.Socket.sendall(self.Crypto.encrypt(Response + "\n"))

                elif re.match(r'get', Sets[0], re.I) != None :

                    if len(Sets) != 2 :
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else :
                        Response = self.Download.GetFile(Sets[1], "ali")
                        self.Socket.sendall(self.Crypto.encrypt(Response + "\n"))