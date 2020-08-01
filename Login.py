import datetime
import base64

#client sent this command to server : Login "Username" "Password" . we decrypt this message and send "Username","password" and socket 
#and crypto module to the ServerLogin class. 
class serverLogin:

    def Login(self,username, password, crypto, Loger): ## main login process

        Loger.Login_Auditor(username, 0)

        #backOff
        returnvalue = self.loginProcess(username, password, crypto)  ## login proccess method
             # 0 for not successful login , 1 for username not found , 2 for incorrect password , 3 for successfull login
        if returnvalue[0] == 0:
            return "Something was wrong, try again \n"

        elif returnvalue[0] == 1:
            return "username Not found, you must sign up first\n"

        if returnvalue[0] == 2: #incorrect password

            ret = ""
            with open("Users.txt", "r") as file:
                list_of_lines = file.readlines()
                set = list_of_lines[returnvalue[1]-1].split(";")

                if (int(set[5]) >= 2 and int(set[5]) <=6) or (int(set[5]) > 6 and set[6] >= str(datetime.datetime.now())) :
                    set[5] = str(int(set[5]) + 1)
                    sec = pow(2, int(set[5]) + 3)
                    sec_added = datetime.timedelta(seconds=sec)
                    Next_Time = datetime.datetime.now() + sec_added
                    list_of_lines[returnvalue[1]-1] = set[0] + ";" + set[1] + ";" + set[2] + ";" + set[3] + ";" + set[4] + ";" + set[5] + ";" + str(Next_Time) + "\n"
                    ret = "The number of attempts is more than allowed !!! Try again later\n"

                elif int(set[5]) > 6 and set[6] < str(datetime.datetime.now()) :
                    set[5] = str(int(set[5]) + 1)
                    sec = pow(2, int(set[5]) + 3)
                    sec_added = datetime.timedelta(seconds=sec)
                    Next_Time = datetime.datetime.now() + sec_added
                    list_of_lines[returnvalue[1] - 1] = set[0] + ";" + set[1] + ";" + set[2] + ";" + set[3] + ";" + set[
                        4] + ";" + set[5] + ";" + str(Next_Time) + "\n"

                    Loger.Login_Auditor(username, 1)
                    ret = "HoneyPot\n"

                elif int(set[5]) <= 2 :
                    list_of_lines[returnvalue[1]-1] = set[0] + ";" + set[1] + ";" + set[2] + ";" + set[3] + ";" + set[4] + ";" + str(int(set[5])+1) + ";" + set[6]
                    ret = "You have entered incorrect password \n"

            a_file = open("Users.txt", "w")
            a_file.writelines(list_of_lines)
            a_file.close()

            return ret


        if returnvalue[0] == 3:# successful login

            with open("Users.txt", "r") as file:
                list_of_lines = file.readlines()
                set = list_of_lines[returnvalue[1]-1].split(";")
                if set[6] >  str(datetime.datetime.now()):
                    return "The number of attempts is more than allowed !!! Try again later\n"

                list_of_lines[returnvalue[1]-1] = set[0] + ";" + set[1] + ";" + set[2] + ";" + set[3] + ";" + set[4] + ";0;" + str(datetime.datetime.now()) + "\n"

            a_file = open("Users.txt", "w")
            a_file.writelines(list_of_lines)
            a_file.close()

            return "Logged in successfully\n"


    def loginProcess(self, username, password, crypto):
        successLogin = 0 # 0 for not successful login , 1 for username not found , 2 for incorrect password , 3 for successfull login
        found = False # for username detection
        LineNumber = 0;
        with open("Users.txt", "r") as file:
            lines = file.readlines()

            for theSet in lines :
                LineNumber = LineNumber + 1
                try:
                    usr,conf,integ,salt,hashedPass, tryNumber, Date = theSet.split(";")
                   # print(usr)
                    #print(username)
                except:
                    successLogin = 0  ## some thing was wrong
                    return successLogin, ""

                if username == usr:
                    temp = base64.b64encode(crypto.sha256(password + salt)).decode()

                    if temp == hashedPass:
                        successLogin = 3 ## correct password -> login successfuly
                        return successLogin, LineNumber
                    else:
                        successLogin = 2 ##incorrect password
                        return successLogin, LineNumber


        successLogin = 0  ## some thing was wrong
        return successLogin, ""