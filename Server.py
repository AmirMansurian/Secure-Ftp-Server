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
import DACCommands
import Auditor
import os
from os import system

KEY_THRESHOLD = 2


class Server:

    def __init__(self, Socket, Crypto, Register, Login, Download, Upload, List, Read, Write, SessionKeyGen, Dac, Loger):

        self.Socket = Socket
        self.Crypto = Crypto
        self.Register = Register
        self.Login = Login
        self.Upload = Upload
        self.Download = Download
        self.List = List
        self.Read = Read
        self.Write = Write
        self.Dac = Dac
        self.Loger = Loger
        self.ConnectedUser = ""
        self.UserConf = ""
        self.UserInteg = ""
        self.IsHoneyPot = 0
        self.SessionKeyGen = SessionKeyGen
        self.fresh_key = 0

        # Key exchange class initilization
        # for session key generation.
        self.SessionKeyGen.sock = self.Socket

    def SetConnectedUser(self, Username):

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

    def Handler(self):

        # Generating first session key
        self.Crypto.key = self.SessionKeyGen.new_session()

        while 1:
           # print(self.Crypto.key)
            Encrypted = self.Socket.recv(4096)
            Command = self.Crypto.decrypt(Encrypted)

            #print(Command)
            if Command == -1:
                self.Socket.sendall(self.Crypto.encrypt("Please try again !!!\n"))

            else:

                Sets = Command.split(" ")

                if re.match(r'register', Sets[0], re.I) != None:

                    if len(Sets) != 5:
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else:
                        Response = self.Register.Registeration(Sets[1:], self.Crypto)
                        self.Socket.sendall(self.Crypto.encrypt(Response))

                elif re.match(r'login', Sets[0], re.I) != None:

                    if len(Sets) != 3:
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else:
                        Response = self.Login.Login(Sets[1], Sets[2], self.Crypto, self.Loger)
                        if Response == "Logged in successfully\n":
                            self.SetConnectedUser(Sets[1])
                            self.Socket.sendall(self.Crypto.encrypt(Response))

                        elif Response == "HoneyPot\n":
                            self.Socket.sendall(self.Crypto.encrypt("Logged in successfully\n"))
                            self.IsHoneyPot = 1
                            self.SetConnectedUser(Sets[1])

                        else:
                            self.Socket.sendall(self.Crypto.encrypt(Response))

                elif re.match(r'list', Sets[0], re.I) != None:

                    if self.ConnectedUser == "":
                        self.Socket.sendall(
                            self.Crypto.encrypt("You should Login/Signin first (use Register/Login command) !!!\n"))

                    elif len(Sets) > 2:
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else:
                        arg = ""
                        if len(Sets) == 2:
                            arg = Sets[1]
                        Response = self.List.GetList(arg, self.ConnectedUser, self.UserConf, self.IsHoneyPot)
                        self.Socket.sendall(self.Crypto.encrypt(Response))

                elif re.match(r'put', Sets[0], re.I) != None:

                    if self.ConnectedUser == "":
                        self.Socket.sendall(
                            self.Crypto.encrypt("You should Login/Signin first (use Register/Login command) !!!\n"))

                    elif len(Sets) != 4:
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else:
                        Response = self.Upload.PutFile(Sets[1:], self.ConnectedUser, self.Loger, self.IsHoneyPot)
                        self.Socket.sendall(self.Crypto.encrypt(Response))

                elif re.match(r'get', Sets[0], re.I) != None:

                    if self.ConnectedUser == "":
                        self.Socket.sendall(
                            self.Crypto.encrypt("You should Login/Signin first (use Register/Login command) !!!\n"))

                    elif len(Sets) != 2:
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else:
                        Response = self.Download.GetFile(Sets[1], self.ConnectedUser, self.Loger, self.IsHoneyPot)
                        self.Socket.sendall(self.Crypto.encrypt(Response))

                elif re.match(r'read', Sets[0], re.I) != None:

                    if self.ConnectedUser == "":
                        self.Socket.sendall(
                            self.Crypto.encrypt("You should Login/Signin first (use Register/Login command) !!!\n"))

                    elif len(Sets) != 2:
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else:
                        Response = self.Read.ReadFromFile(self.ConnectedUser, Sets[1], self.UserConf, self.UserInteg,
                                                          self.Loger, self.IsHoneyPot)
                        self.Socket.sendall(self.Crypto.encrypt(Response))

                elif re.match(r'write', Sets[0], re.I) != None:

                    Sets2 = Command.split("\"")
                    if self.ConnectedUser == "":
                        self.Socket.sendall(
                            self.Crypto.encrypt("You should Login/Signin first (use Register/Login command) !!!\n"))

                    elif len(Sets2) == 1:

                        Sets3 = Sets2[0].split(" ")
                        if len(Sets3) != 3:
                            self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                        else:
                            Response = self.Write.WriteToFile(self.ConnectedUser, Sets3[1:], self.UserConf,
                                                              self.UserInteg,
                                                              self.Loger, self.IsHoneyPot)
                            self.Socket.sendall(self.Crypto.encrypt(Response))

                    elif len(Sets2) == 3:

                        Sets3 = Sets2[0].split(" ")
                        if len(Sets3) != 3:
                            self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                        else:
                            temp = [""] * 2
                            temp[0] = Sets3[1]
                            temp[1] = Sets2[1]
                            print(temp[0], temp[1])
                            Response = self.Write.WriteToFile(self.ConnectedUser, temp, self.UserConf, self.UserInteg,
                                                              self.Loger, self.IsHoneyPot)
                            self.Socket.sendall(self.Crypto.encrypt(Response))

                elif re.match(r'grant', Sets[0], re.I) != None:

                    if self.ConnectedUser == "":
                        self.Socket.sendall(
                            self.Crypto.encrypt("You should Login/Signin first (use Register/Login command) !!!\n"))

                    elif len(Sets) != 4:
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else:
                        Response = self.Dac.GrantAccess(self.ConnectedUser, Sets[1:], self.Loger, self.IsHoneyPot)
                        self.Socket.sendall(self.Crypto.encrypt(Response))

                elif re.match(r'revoke', Sets[0], re.I) != None:

                    if self.ConnectedUser == "":
                        self.Socket.sendall(
                            self.Crypto.encrypt("You should Login/Signin first (use Register/Login command) !!!\n"))

                    elif len(Sets) != 4:
                        self.Socket.sendall(self.Crypto.encrypt("inappropriate arguments !!!\n"))
                    else:
                        Response = self.Dac.RevokeAccess(self.ConnectedUser, Sets[1:], self.Loger, self.IsHoneyPot)
                        self.Socket.sendall(self.Crypto.encrypt(Response))

                elif re.match(r'exit', Sets[0], re.I) != None:
                    self.IsHoneyPot = 0
                    self.ConnectedUser = ""
                    self.Socket.sendall(self.Crypto.encrypt("Bye Bye !!!\n".encode()))

                else:
                    self.Socket.sendall(self.Crypto.encrypt(Sets[0] + " is not a built-in command !!!\n"))

            # Increase session key lifetime and generate
            # a new one if needed at the end of this loop 
            self.fresh_key += 1
            if (self.fresh_key > KEY_THRESHOLD):
                self.fresh_key = 0
                self.Crypto.key = self.SessionKeyGen.key_freshness()


def check_files_and_folders():
        if not os.path.exists('Files'):
            os.makedirs('Files')
        if not os.path.exists('Logs'):
            os.makedirs('Logs')
        if not os.path.exists('Fake'):
            os.makedirs('Fake')
        if not os.path.exists('Fake/Logs'):
            os.makedirs('Fake/Logs')
        if not os.path.exists('Fake/Files'):
            os.makedirs('Fake/Files')
        
        try:
            file = open('Logs/Auth_log.txt', 'r')
        except FileNotFoundError:
            file = open('Logs/Auth_log.txt', 'w')
        file.close()

        try:
            file = open('Logs/FileTransfer_log.txt', 'r')
        except FileNotFoundError:
            file = open('Logs/FileTransfer_log.txt', 'w')
        file.close()

        try:
            file = open('Fake/Logs/FileTransfer_log.txt', 'r')
        except FileNotFoundError:
            file = open('Fake/Logs/FileTransfer_log.txt', 'w')
        file.close()

        try:
            file = open('Users.txt', 'r')
        except FileNotFoundError:
            file = open('Users.txt', 'w')
        file.close()


def __main__():
    check_files_and_folders()
    socket = Socket.ServerSocket()
    connection = socket.Socket()
    sr = Server(connection, Cryptography.session_crypto(None), Registery.Registery(), Login.serverLogin(),
                Download.Download(), Upload.Upload(), List.List(), Read.Read(), Write.Write(),
                SessionKeyExchange.ServerSession(None),
                DACCommands.DACCommands(), Auditor.Auditor())
    sr.Handler()


__main__()
