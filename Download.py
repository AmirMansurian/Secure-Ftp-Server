import os

class Download :

    def GetFile (self, FileName, Owner) :

        if self.FileNameCheck(FileName) == -1 :
           return "File Not Found !!!\n"

        if self.OwnerCheck(Owner, FileName) == -1 :
           return "Permission Denied !!!\n"

        os.remove("Files/" + FileName + ".txt")

        return FileName + ".txt Removed from Server Successfully !!!\n"


    def FileNameCheck (self, FileName) :
        IsValid = -1
        dir = os.listdir('Files/')
        for names in dir :
            if FileName + ".txt" == names :
                IsValid = 1
        return IsValid

    def OwnerCheck (self, Owner, FileName) :
        dir = os.listdir('Files/')
        for names in dir:
            if FileName + ".txt" == names :
                File = open("Files/" + names, "r")
                line = File.readline()
                set = line.split(" ")
                if set[0] == Owner :
                    return 1
                return -1