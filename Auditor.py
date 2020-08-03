import datetime
import os


class Auditor :


    def Login_Auditor(self, Username, IsHoneyPot):

        if IsHoneyPot == 0 :
            Number_try = 0
            File = open("Users.txt", "r")
            Lines = File.readlines()
            for line in Lines :

                set = line.split(";")

                if Username == set[0]:
                    Number_try = set[5]
                    break

            File.close()

            if int(Number_try) >= 3 and set[6] >= str(datetime.datetime.now()):
                print("[" + str(datetime.datetime.now()) + "] " + Username + " had unsuccessfull login " + str(Number_try) + " times\n")

            File = open("Logs/Auth_log.txt", "a")
            File.write(str(datetime.datetime.now()) + ";" + Username + ";login\n")
            File.close()

        else :

            print("[" + str(datetime.datetime.now()) + "] " + "User " + Username + " Entered HoneyPot Mode(Check for actions in Fake/Logs/) !!!\n")
            File = open("Logs/Auth_log.txt", "a")
            File.write(str(datetime.datetime.now()) + ";" + Username + ";HoneyPot\n")
            File.close()


    def Put_Get_Audit (self, Owner, FileName, Operation, IsHoneyPot) :

        if IsHoneyPot == 0 :
            File = open("Logs/FileTransfer_log.txt", "a")
        else :
            File = open("Fake/Logs/FileTransfer_log.txt", "a")

        File.write(str(datetime.datetime.now()) + ";" +Owner + ";tried to;" + Operation + ";" + FileName + ";\n")
        File.close()

        if '\\' in FileName or '/' in FileName:
            print("[" + str(datetime.datetime.now()) + "] " + "Path_Traversal : " + Owner + " tried to " + Operation + " " + FileName + "\n")

        if IsHoneyPot ==0 :
            counter = 0
            if Operation == "Put" :

                File = open("Logs/FileTransfer_log.txt", "r")

                list_of_lines = File.readlines()
                index = len(list_of_lines)-1

                while index >0 :
                    set = list_of_lines[index].split(";")
                    if set[1] == Owner and set[3] == Operation and set[4] and str(datetime.datetime.now() - datetime.timedelta(1)) <= set[0]:
                        counter = counter + 1
                    index = index - 1

                File.close()

            if counter >= 20:
                print(
                    "[" + str(datetime.datetime.now()) + "] " + "User " + Owner + " tried to " + Operation + " the file " +  str(counter) + " times in last 24 hour\n")
                return -1

        return 1


    def Read_Write_Auditor(self, username, user_conf, user_integ, filename, file_conf, file_integ, user_acl, operation, IsHoneyPot):
        # Log command
        # Log fromat:
        # Time;Operation;Username;UserConf;UserInteg;Filename;FileConf;FileInteg
        if IsHoneyPot == 1:
            logs_file = "Fake/Logs/ReadWrite_log.txt"
        else:
            logs_file = "Logs/ReadWrite_log.txt"
        try:
            file = open(logs_file, 'a')
        except FileNotFoundError:
            file = open(logs_file, 'w')
        if (len(file_conf) == 0 or len(file_integ) == 0):
            file.write(str(datetime.datetime.now()) + ";" + operation + ';' + username + ';' +
                      user_conf[1:] + ';' +
                     user_integ[1:] + ';' +
                     filename + ';' + 
                     'no such file;\n')
            file.close()
        else:
            file.write(str(datetime.datetime.now()) + ";" + operation + ';' + username + ';' +
                      user_conf[1:] + ';' +
                     user_integ[1:] + ';' +
                     filename + ';' + 
                     file_conf[1:] + ';' +
                    file_integ[1:] + ';' + user_acl + '\n')
        file.close()

        # Audit command
        # Audit path traversal attack 
        if '\\' in filename or '/' in filename:
            print("[" + str(datetime.datetime.now()) + "] " + "Path Traversal : " + username + " tried to " +
                 operation + " " + filename + "\n")
            return 1
        
        # If file doesn't exist and there is no path travesal attack
        if (len(file_conf) == 0 or len(file_integ) == 0):
            print(print("[" + str(datetime.datetime.now()) + "] " + username + " tried to " +
                 operation + " " + filename + " that doesn't exist.\n"))
            return 1
        
        if operation == 'write' and user_acl != 'No DAC' and 'w' not in user_acl:
            print("[" + str(datetime.datetime.now()) + "] " + "DAC violation attempt by " + username + " tried to " +
                 operation + " " + filename + "\n")
            return 1

        if operation == 'read' and user_acl != 'No DAC' and 'r' not in user_acl:
            print("[" + str(datetime.datetime.now()) + "] " + "DAC violation attempt by " + username + " tried to " +
                 operation + " " + filename + "\n")
            return 1
      
        # If DAC is set for the file and the user has the appropriate
        # right, then there is no violation
        if operation == 'read' and 'r' in user_acl:
            return 1
        elif operation == 'write' and 'w' in user_acl:
            return 1

        # Audit attack against mandatory access control
        if (operation == 'write'):
            if (user_conf[0] > file_conf[0]):
                if (user_integ[0] < file_integ[0]):
                    print("[" + str(datetime.datetime.now()) + "] " + "Confidentiality and integrity violation attempt by " 
                          + username + " on " + filename + " : Write attemp")
                else:
                    print("[" + str(datetime.datetime.now()) + "] " + "Confidentiality violation attempt by " 
                          + username + " on " + filename + " : Write attemp")
            elif (user_integ[0] < file_integ[0]):
                print("[" + str(datetime.datetime.now()) + "] " + "Integrity violation attempt by " +
                     username + " on " + filename + " : Write attemp")

        elif (operation == 'read'):
            if (user_conf[0] < file_conf[0]):
                if (user_integ[0] > file_integ[0]):
                    print("[" + str(datetime.datetime.now()) + "] " + "Confidentiality and integrity violation attempt by " + username 
                    + " on " + filename + " : Read attemp")
                else:
                    print("[" + str(datetime.datetime.now()) + "] " + "Confidentiality violation attempt by " + username 
                          + " on " + filename + " : Read attemp")
            elif (user_integ[0] > file_integ[0]):
                print("[" + str(datetime.datetime.now()) + "] " + "Integrity violation attempt by " + username 
                      + " on " + filename + " : Read attemp")

        return 1


    def Revoke_Grant_Audit(self, source_user, permission, file_name, file_owner, target_user, operation, IsHoneyPot):
        if IsHoneyPot == 1:
            logs_file = "Fake/Logs/DACCommands_Log.txt"
        else:
            logs_file = "Logs/DACCommands_Log.txt.txt"

        try:
            file = open(logs_file, 'a')
        except FileNotFoundError:
            file = open(logs_file, 'w')

        file.write(str(datetime.datetime.now()) + ";" + operation + ';' + source_user + ';' +
                   target_user + ';' +
                   permission + ';' +
                   file_name + ';' + file_owner + ';\n')
        file.close()

        # Audit path traversal
        if '\\' in file_name or '/' in file_name:
            print("[" + str(datetime.datetime.now()) + "] " + "Path Traversal : " + source_user + " tried to " +
                  operation + " " + file_name + "\n")
            return 1

        # If file doesn't exist and there is no path travesal attack
        if (len(file_owner) == ''):
            print(print("[" + str(datetime.datetime.now()) + "] " + source_user + " tried to " +
                        operation + " DAC permissions on/from " + file_name + " that doesn't exist.\n"))
            return 1

        if (file_owner != source_user):
            print("[" + str(datetime.datetime.now()) + "] " + source_user + ' attemp to change dac'
                  + " on " + file_name + " which is not the owner of")
        return 1
            