import re
import time
import socket

class ServerRegistery:

    def __init__(self):
        Socket = socket.socket()
        Socket.bind(('0.0.0.0', 12345))
        Socket.listen(1)
        Client, Adder = Socket.accept()
        print("Client with adder : " + Adder + " Connected !!!\n")
        self.Menu(Socket)

    def Menu(self, Socket):

            while (1) :
                Socket.sendall("Welcome to Server Registery Serveice \n Please Enter your Username : \n".encode())
                Username = Socket.recv(1024)
                if  self.UsernameCheck(Username) == 1:
                    break
                else :
                    Socket.sendall("This Username is already taken\n".encode())
                    time.sleep(3)


            flag = 1
            while (flag):
                while (1) :
                    Socket.sendall("Please Enter your Password : \n".encode())
                    Password = Socket.recv(1024)
                    if self.PassCheck(Username, Password) == 1 :
                        break
                    else :
                        Socket.sendall("Password you have choosed is weak !!! Please choose anotherone\n".encode())

                while (1) :
                    Socket.sendall("Please re-enter your password : \n".encode())
                    if Password == Socket.recv(1024):
                        Socket.sendall("Registered !!!\n".encode())

                        File = open ("users.txt", "r")
                        Salt = 1
                        while 1:
                            line = File.readline()
                            if not line:
                                break
                            Salt = Salt + 1
                        File.close()

                        File = open("Users.txt", "a")
                        File.write(Username + ":" + str(Salt) + ":" + Password)
                        File.close()

                        flag = 0
                        break
                    else :
                        Socket.sendall("Repeated Password is  not the same as Password !!!\n".encode())
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

        if re.match(r'(.*)' + UsernamePattern, Password) :
            IsValid = -1

        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', Password):
            IsValid = -1

        return IsValid



class ClientRegistery :

    def  __init__(self):
        Socket = socket.socket()
        Socket.connect(('localhost', 12345))
        self.Menu(Socket)

    def Menu (self, Socket) :

        while (1):
            print(Socket.recv(1024))
            Username = input()
            Socket.sendall(Username.encode())
            if Socket.recv(1024) == "Please Enter your Password : \n" :
                break
            else :
                print("This Username is already taken\n")

        flag = 1
        while (flag):
            while (1):
                print("Please Enter your Password : \n")
                Password = input()
                Socket.sendall(Password.encode())
                if Socket.recv(1024) == "Please re-enter your password : \n" :
                    break
                else :
                    print("Password you have choosed is weak !!! Please choose anotherone\n")

            while (1):
                print("Please re-enter your password : \n")
                Password = input()
                Socket.sendall(Password.encode())
                if Socket.recv(1024) == "Registered !!!\n" :
                    print("Registered !!!\n")
                    flag = 0
                    break
                else :
                    print("Repeated Password is  not the same as Password !!!\n")
                    break
        return 1


p = ServerRegistery()
print(p.Menu())
