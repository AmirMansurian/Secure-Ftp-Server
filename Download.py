import os

class Download :

    def GetFile (self, FileName, Owner, logger) :

        logger.Put_Get_Audit(Owner, FileName, "Get")

        # Check for path traversal attack
        if '\\' in FileName or '/' in FileName:
            return "Invalid file name"

        if self.FileNameCheck(FileName) == -1 :
           return "File Not Found !!!\n"

        if self.OwnerCheck(Owner, FileName) == -1 :
           return "Permission Denied !!!\n"

        file = open("Files/" + FileName, "r")
        file_acl = file.readline()
        file_acl = file.readline()
        file.close()
        if self._CheckDiscretionaryAccess(file_acl, Owner) == -1:
            return "Permission Denied!(By discretionary access control rules)\n"

        os.remove("Files/" + FileName)

        return FileName + ".txt Removed from Server Successfully !!!\n"


    def FileNameCheck (self, FileName) :
        IsValid = -1
        dir = os.listdir('Files/')
        for names in dir :
            if FileName == names :
                IsValid = 1
        return IsValid

    def OwnerCheck (self, Owner, FileName) :
        dir = os.listdir('Files/')
        for names in dir:
            if FileName == names :
                File = open("Files/" + names, "r")
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
