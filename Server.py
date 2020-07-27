import re
import List
import Socket
import Cryptography
import Registery
import Login
import Download
import Upload
import Read
import Write


class Server :

    def __init__(self, Socket, Crypto, Register, Login, Download, Upload, Read, Write, List):

        self.Socket = Socket
        self.Crypto = Crypto
        self.Register = Register
        self.Login = Login
        self.Upload = Upload
        self.Download = Download
        self.Read = Read
        self.Write = Write
        self.List = List
        self.ConnectedUser = ""
        self.UserConf = ""
        self.UserInteg = ""


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
