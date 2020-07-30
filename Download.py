import os

class Download :

    def GetFile (self, FileName, Owner, logger, IsHoneyPot) :

        logger.Put_Get_Audit(Owner, FileName, "Get", IsHoneyPot)

        # Check for path traversal attack
        if '\\' in FileName or '/' in FileName:
            return "Invalid file name\n"

        if self.FileNameCheck(FileName, IsHoneyPot) == -1 :
           return "File Not Found !!!\n"

        if self.OwnerCheck(Owner, FileName, IsHoneyPot) == -1 :
           return "Permission Denied !!!\n"

        path = ""
        if IsHoneyPot == 0:
            file = open("Files/" + FileName, "r")
            path = "Files/"
        else :
            file = open("Fake/Files/" + FileName, "r")
            path = "Fake/Files/"

        file_acl = file.readline()
        file_acl = file.readline()
        file.close()
        if self._CheckDiscretionaryAccess(file_acl, Owner) == -1:
            return "Permission Denied!(By discretionary access control rules)\n"

        os.remove(path + FileName)

        return FileName + ".txt Removed from Server Successfully !!!\n"


    def FileNameCheck (self, FileName, IsHoneyPot) :
        IsValid = -1
        if IsHoneyPot == 0 :
            dir = os.listdir('Files/')
        else :
            dir = os.listdir('Fake/Files/')

        for names in dir :
            if FileName == names :
                IsValid = 1
        return IsValid

    def OwnerCheck (self, Owner, FileName, IsHoneyPot) :

        path = ""
        if IsHoneyPot == 0 :
            dir = os.listdir('Files/')
            path = "Files/"
        else :
            dir = os.listdir('Fake/Files/')
            path = "Fake/Files/"

        for names in dir:
            if FileName == names :
                File = open(path + names, "r")
                line = File.readline()
                set = line.split(" ")
                if set[0] == Owner :
                    return 1
                return -1

    def _CheckDiscretionaryAccess(self, acl, username):
        index = acl.find(username + ':')
        if index == -1:
            return 1

        user_acl = acl[ index + len(username) + 1 : index + len(username) + 4]
        if 'g' in user_acl:
            return 1
        return -1
