import datetime
import os


class Auditor :


    def Login_Auditor(self, Username):

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


    def Put_Get_Audit (self, Owner, FileName, Operation) :

        counter = 0
        File = open("Logs/FileTransfer_log.txt", "a")
        File.write(str(datetime.datetime.now()) + ";" +Owner + ";tried to;" + Operation + ";" + FileName + ";\n")
        File.close()

        if '\\' in FileName or '/' in FileName:
            print("[" + str(datetime.datetime.now()) + "] " + "Path_Traversal : " + Owner + " tried to " + Operation + " " + FileName + "\n")

        if Operation == "Get":

            admin = ""
            dir = os.listdir('Files/')
            if FileName not in dir :

                File = open("Logs/FileTransfer_log.txt", "r")

                list_of_lines = File.readlines()

                for line in list_of_lines:
                    set = line.split(";")
                    if set[1] == Owner and set[3] == Operation and set[4] == FileName and str(datetime.datetime.now() - datetime.timedelta(1)) <= set[0]:
                        counter = counter + 1

                File.close()

            if counter >= 5:
                print(
                    "[" + str(datetime.datetime.now()) + "] " + "User " + Owner + " tried to " + Operation + " " + FileName,
                    " (that doesnt exist) " + str(counter) + " times in last 24 hour\n")
                return -1

            if FileName in dir :
                counter = 0
                File = open("Files/" + FileName, "r")
                list_of_lines = File.readline()
                set = list_of_lines.split(" ")
                admin = set[0]
                File.close()

                if admin!= Owner:

                    File = open("Logs/FileTransfer_log.txt", "r")

                    list_of_lines = File.readlines()

                    for line in list_of_lines:
                        set = line.split(";")

                        if set[1] == Owner and set[3] == Operation and set[4] == FileName and str(datetime.datetime.now() - datetime.timedelta(1)) <= set[0]:
                            counter = counter + 1

                    File.close()

                if counter >= 5 :
                    print("[" + str(datetime.datetime.now()) + "] " + "User " + Owner + " tried to " + Operation + " " + FileName, " (that is not his/her own file) " + str(counter) + " times in last 24 hour\n")
                    return -1

        counter = 0
        if Operation == "Put" :
            dir = os.listdir('Files/')
            if FileName in dir :

                File = open("Logs/FileTransfer_log.txt", "r")

                list_of_lines = File.readlines()

                for line in list_of_lines:
                    set = line.split(";")

                    if set[1] == Owner and set[3] == Operation and set[4] == FileName and str(
                            datetime.datetime.now() - datetime.timedelta(1)) <= set[0]:
                        counter = counter + 1

                File.close()


        if counter >= 5:
            print(
                "[" + str(datetime.datetime.now()) + "] " + "User " + Owner + " tried to " + Operation + " " + FileName,
                " (that alrealdy exist) " + str(counter) + " times in last 24 hour\n")
            return -1

        return 1



