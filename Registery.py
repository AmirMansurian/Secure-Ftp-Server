import re
import datetime
import base64
import Cryptography

class Registery:

    def Registeration(self, Args, crypto):

        Username = Args[0];
        Password = Args[1];
        ConfLevel = Args[2];
        IntegLevel = Args[3];

        if self.UsernameCheck(Username) == -1 :
            return "This username is already taken !!!\n"

        if self.PassCheck(Username, Password) == -1 :
            return "Password you have choosed is a weak password !!! please chosse anotherone\n"

        if re.match(r'TopSecret', ConfLevel, re.I) == None and re.match(r'Secret', ConfLevel, re.I) == None and re.match(r'Confidential', ConfLevel, re.I) == None and re.match(r'Unclassified', ConfLevel, re.I) == None :
            return "Confidentiality level is not Valid !!!\n"

        if re.match(r'VeryTrusted', IntegLevel, re.I) == None and re.match(r'Trusted', IntegLevel,re.I) == None and re.match(r'SlightlyTrusted',IntegLevel,re.I) == None and re.match(r'Untrusted', IntegLevel, re.I) == None:
                return "Integrity level is not Valid !!!\n"

        File = open("users.txt", "r")
        Salt = 1
        while 1:
            line = File.readline()
            if not line:
                break
            Salt = Salt + 1
        File.close()

        File = open("Users.txt", "a")
        File.write(Username + ";" + ConfLevel + ";" + IntegLevel + ";" + str(Salt) + ";" + base64.b64encode(crypto.sha256(Password + str(Salt))).decode() + ";0;" + str(datetime.datetime.now()) + "\n")
        File.close()

        return "Registered !!!\n"


    def UsernameCheck(self, Username):

        Isvalid = 1

        File = open("Users.txt", "r")
        while 1 :
            line = File.readline()

            if not line :
                break

            set = line.split(";")
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


a = Registery()
c = Cryptography.session_crypto("key")

set = [""]*4
set[0] = "soheil"
set[1] = "Amir@1377"
set[2] = "TopSecret"
set[3] = "VeryTrusted"

print(a.Registeration(set, c))
