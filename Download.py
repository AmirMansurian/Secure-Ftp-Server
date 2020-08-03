import os
import Read

class Download :

    def GetFile (self, FileName, Owner, user_conf, user_integ, logger, IsHoneyPot, Read) :

        logger.Put_Get_Audit(Owner, FileName, "Get", IsHoneyPot)

        path = ""
        if IsHoneyPot == 0 :
            self.dir = "Files/"
        else :
            self.dir = "Fake/Files/"

        # Check for path traversal attack
        if '\\' in FileName or '/' in FileName:
            return "Invalid file name\n"

        if self.FileNameCheck(FileName) == -1:
           return "File Not Found !!!\n"

        if self.OwnerCheck(Owner, FileName) == -1 and self._CheckDiscretionaryAccess(file_acl, Owner) == -1:
           return "Permission Denied !!!\n"

        file = open(self.dir + FileName, "r")
        file_acl = file.readline()
        file_acl = file.readline()
        file.close()
        if self._CheckDiscretionaryAccess(file_acl, Owner) == -1:
            return "Permission Denied!(By discretionary access control rules)\n"

        file_content = Read.ReadFromFile(Owner, FileName, user_conf, user_integ, logger, IsHoneyPot)

        os.remove(self.dir + FileName)

        return FileName + " Removed from Server Successfully !!!\n" + file_content


    def FileNameCheck (self, FileName) :

        IsValid = -1

        dir = os.listdir(self.dir)
        for names in dir :
            if FileName == names :
                IsValid = 1
        return IsValid

    def OwnerCheck (self, Owner, FileName) :

        dir = os.listdir(self.dir)
        for names in dir:
            if FileName == names :
                File = open(self.dir + names, "r")
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
