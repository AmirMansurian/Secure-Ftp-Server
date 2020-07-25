import time
import base64
import sys
import time

## must be global values of main programm
timervalue = 1
j = 1 #exponentioal power for timer value
##

#client sent this command to server : Login "Username" "Password" . we decrypt this message and send "Username","password" and socket 
#and crypto module to the ServerLogin class. 
class serverLogin:
    

    def __init__(self, crypto, clientSocket,username, password):
        self.crypto = crypto
        self.clientSocket = clientSocket
        self.Login(self,username,password)

    def Login(self,username, password): ## main login process
        #backOff
        while True:

            returnvalue = self.loginProcess(username, password)  ## login proccess method  
             # 0 for not successful login , 1 for username not found , 2 for incorrect password , 3 for successfull login
            if returnvalue == 0:
                self.clientSocket.sendall(self.crypto.encrypt("Something was wrong, try again \n"))
                break
            if returnvalue == 1:
                self.clientSocket.sendall(self.crypto.encrypt("username Not found, you must sign up first"))
                break
            if returnvalue == 2: #incorrect password
                self.clientSocket.sendall(self.crypto.encrypt("incorrect password, you can sign in again after"+ str(timervalue) + "seconds"))
                self.timedelay(timervalue)
                timervalue =  2**j
                j = j + 1 
                break    ####################################
            if returnvalue == 3:# successful login
                self.clientSocket.sendall(self.crypto.encrypt("Logged in successfully"))
                break





    def loginProcess(self, username, password):
        successLogin = 0 # 0 for not successful login , 1 for username not found , 2 for incorrect password , 3 for successfull login
        found = False # for username detection
        with open("Users.txt", "r") as file:
            for x in file:
                 theSet = x.readline()
                 try:
                    usr,conf,integ,salt,hashedPass = theSet.split(":")
                 except:
                     successLogin = 0  ## some thing was wrong
                     return successLogin
                                 
                 if username == usr:
                     found = True
                     temp = base64.b64encode(self.crypto.sha256(password + salt)).decode()

                     if temp == hashedPass:

                         successLogin = 3 ## correct password -> login successfuly
                         return successLogin
                     else:
                         successLogin = 2 ##incorrect password
                         return successLogin
            if found == False:
                successLogin = 1 ## user not found 
                return successLogin
        return 0



    def timedelay(self,x):
        while x >= 0:
          #  print("You can try again in " + str(x) + "seconds...")
           # x = x - 1
            #sys.stdout.write("\033[K") # Clear to the end of line
            time.sleep(1)
