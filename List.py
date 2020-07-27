import os

class List :

    def GetList (self) :

        dir = os.listdir('Files/')
        Result = ""

        for file in dir :

            File = open("Files/" + file, "r")
            line = File.readline()
            if not line:
                break

            set = line.split(" ")
            Result += file + "      " + set[0] + "/" + set[1] + "/" + set[2] + "\n"
            File.close()

        return Result