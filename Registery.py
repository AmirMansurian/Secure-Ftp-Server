import re

class Registery:
    def __init__(self):
        print()

    def Menu(self):

        while 1 :
            print("Welcome to Server Registery !!!")
            Username = input("Please Enter your Username : ")


            Password = input("Please Enter your Password : ")

            if Password == (input("Please re-enter your password : ")):
                print("Registered !!!")
            else :
                print("pass incorrect")


    def UsernameCheck(self, Username):

        Isvalid = -1

        File = open("Users.txt", "r")
        while 1 :
            line = File.readline()

            if not line :
                break

            set = line.split(":")
            print(set[0])
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

        File = open("Users.txt", "r")
        while 1:
            line = File.readline()
            if not line:
                break

            set = line.split(":")

            if (Password == set[1][0: len(set[1]) - 1]):
                IsValid = -1

        File.close()
        return IsValid

p = Registery()
print(p.PassCheck("ali", "Amairl@13i77"))
print(p.UsernameCheck("amir"))