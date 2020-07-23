import re
import time
import base64

class ServerRegistery:

    def __init__(self, socket, crypto):
        self.Menu(socket, crypto)

    def Menu(self, Client, crypto):

            while (1) :

                Client.sendall(crypto.encrypt("Welcome to Server Registery Serveice \n Please Enter your Username : \n"))
                Username = crypto.decrypt(Client.recv(1024))
                print(Username)
                if  self.UsernameCheck(Username) == 1:
                    break
                else :
                    Client.sendall(crypto.encrypt("This Username is already taken\n"))


            flag = 1
            while (flag):
                while (1) :
                    Client.sendall(crypto.encrypt("Please Enter your Password : \n"))
                    Password = crypto.decrypt(Client.recv(1024))
                    if self.PassCheck(Username, Password) == 1 :
                        break
                    else :
                        Client.sendall(crypto.encrypt("Password you have choosed is weak !!! Please choose anotherone\n"))

                while (1) :
                    Client.sendall(crypto.encrypt("Please re-enter your password : \n"))
                    if Password == crypto.decrypt(Client.recv(1024)):
                        Client.sendall(crypto.encrypt("Registered !!!\n"))

                        File = open ("users.txt", "r")
                        Salt = 1
                        while 1:
                            line = File.readline()
                            if not line:
                                break
                            Salt = Salt + 1
                        File.close()

                        File = open("Users.txt", "a")
                        File.write(Username + ":" + str(Salt) + ":" + base64.b64encode(crypto.sha256(Password + str(Salt))).decode() + "\n")
                        File.close()

                        flag = 0
                        break
                    else :
                        Client.sendall(crypto.encrypt("Repeated Password is  not the same as Password !!!\n"))
                        break
            return 1

    def UsernameCheck(self, Username):

        Isvalid = 1

        File = open("Users.txt", "r")
        while 1 :
            line = File.readline()

            if not line :
                break

            set = line.split(":")
            if (Username == set[0]) :
                Isvalid =  -1

        File.close()
        return Isvalid

    def PassCheck(self, Username, Password):

        IsValid = 1

        UsernamePattern = "(.*)"
        for char in Username :
            UsernamePattern += char
            UsernamePattern += "(.*)"

        if re.match(r'(.*)' + UsernamePattern, Password, re.I) :
            IsValid = -1

        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', Password):
            IsValid = -1

        return IsValid


class ClientRegistery :

    def  __init__(self, socket, crypto):
        self.Menu(socket, crypto)

    def Menu (self, Socket, crypto) :

        while (1):

            print(crypto.decrypt(Socket.recv(1024)))
            Username = input()
            Socket.sendall(crypto.encrypt(Username))
            if crypto.decrypt(Socket.recv(1024)) == "Please Enter your Password : \n" :
                break
            else :
                print("This Username is already taken\n")

        flag = 1
        while (flag):
            while (1):
                print("Please Enter your Password : \n")
                Password = input()
                Socket.sendall(crypto.encrypt(Password))
                if crypto.decrypt(Socket.recv(1024)) == "Please re-enter your password : \n" :
                    break
                else :
                    print("Password you have choosed is weak !!! Please choose anotherone\n")

            while (1):
                print("Please re-enter your password : \n")
                Password = input()
                Socket.sendall(crypto.encrypt(Password))
                if crypto.decrypt(Socket.recv(1024)) == "Registered !!!\n" :
                    print("Registered !!!\n")
                    flag = 0
                    break
                else :
                    print("Repeated Password is  not the same as Password !!!\n")
                    break
        return 1
