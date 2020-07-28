import re
import SessionKeyExchange
import Socket
import Cryptography
import Registery
import List
import Login
import Download
import Upload
import Read
import Write


KEY_THRESHOLD = 2

class Server :

    def __init__(self, Socket, Crypto, Register, Login, Download, Upload, List, Read, Write, SessionKeyGen):

        self.Socket = Socket
        self.Crypto = Crypto
        self.Register = Register
        self.Login = Login
        self.Upload = Upload
        self.Download = Download
        self.List = List
        self.Read = Read
        self.Write = Write
        self.ConnectedUser = ""
        self.UserConf = ""
        self.UserInteg = ""
        self.SessionKeyGen = SessionKeyGen
        self.fresh_key = 0
        
        # Key exchange class initilization
        # for session key generation. 
        self.SessionKeyGen.sock = self.Socket

        

    def SetConnectedUser (self, Username) :

        self.ConnectedUser = Username
        File = open("Users.txt", "r")
        while 1:
            line = File.readline()

            if not line:
                break

            set = line.split(";")
            if (Username == set[0]):
                self.UserConf = set[1]
                self.UserInteg = set[2]

        File.close()



    def Handler (self) :

        # Generating first session key
        self.Crypto.key = self.SessionKeyGen.new_session()

        while 1 :
            print(self.Crypto.key)
            Encrypted = self.Socket.recv(2048)
            Command = self.Crypto.decrypt(Encrypted)

            print(Command)
            if Command == -1 :
                self.Socket.sendall(self.Crypto.encrypt("Please try again !!!\n"))

            else :

                Sets = Command.split(" ")

                if re.match(r'register', Sets[0], re.I) != None :

                    if len(Sets) != 5 :
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else :
                        Response = self.Register.Registeration(Sets[1:], self.Crypto)
                        self.Socket.sendall(self.Crypto.encrypt(Response))

                elif re.match(r'login', Sets[0], re.I) != None :

                    if len(Sets) != 3 :
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else :
                        Response = self.Login.Login(Sets[1], Sets[2], self.Crypto)
                        self.Socket.sendall(self.Crypto.encrypt(Response))
                        self.SetConnectedUser(Sets[1])

                elif re.match(r'list', Sets[0], re.I) != None :

                    if len(Sets) != 1 :
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else :
                        Response = self.List.GetList()
                        self.Socket.sendall(self.Crypto.encrypt(Response))

                elif re.match(r'put', Sets[0], re.I) != None :

                    if len(Sets) != 4 :
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else :
                        Response = self.Upload.PutFile(Sets[1:], self.ConnectedUser)
                        self.Socket.sendall(self.Crypto.encrypt(Response))

                elif re.match(r'get', Sets[0], re.I) != None :

                    if len(Sets) != 2 :
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else :
                        Response = self.Download.GetFile(Sets[1], self.ConnectedUser)
                        self.Socket.sendall(self.Crypto.encrypt(Response))

                elif re.match(r'read', Sets[0], re.I) != None :

                    if len(Sets) != 2 :
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else :
                        Response = self.Read.ReadFromFile(Sets[1], self.UserConf, self.UserInteg)
                        self.Socket.sendall(self.Crypto.encrypt(Response))

                elif re.match(r'write', Sets[0], re.I) != None :

                    if len(Sets) != 3 :
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else :
                        Response = self.Write.WriteToFile(Sets[1:], self.UserConf, self.UserInteg)
                        self.Socket.sendall(self.Crypto.encrypt(Response))

                else :
                    self.Socket.sendall(self.Crypto.encrypt(Sets[0] + " is not a built-in command !!!\n"))

            # Increase session key lifetime and generate
            # a new one if needed at the end of this loop 
            self.fresh_key += 1
            if (self.fresh_key > KEY_THRESHOLD):
                self.fresh_key = 0
                self.Crypto.key = self.SessionKeyGen.key_freshness()



def __main__():
    socket = Socket.ServerSocket()
    connection = socket.Socket()
    sr = Server(connection, Cryptography.session_crypto(None), Registery.Registery(), Login.serverLogin(),
               Download.Download(), Upload.Upload(), List.List() ,Read.Read(), Write.Write(), SessionKeyExchange.ServerSession(None))
    sr.Handler()

__main__()