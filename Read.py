import os
class Read:
    def ReadFromFile(self, username, filename, user_conf, user_integ, Loger):
        Loger.Read_Write_Auditor(username, self._normalize_level(user_conf), 
                                 self._normalize_level(user_integ), 
                                 self._normalize_level(filename),
                                 self._normalize_level(file_conf), 
                                 self._normalize_level(file_integ), 'read')
                                 
        # Check for path traversal attack
        if '\\' in filename or '/' in filename:
            return "Invalid file name\n"
        
        if self._FileNameCheck(filename) == -1:
            return "File Not Found !!!\n"

        # Read access control data from the file
        file = open("Files/" + filename, "r")
        file_owner, file_conf, file_integ = file.readline().split(' ')
        
        if self._CheckDiscretionaryAccess(file.readline(), username) == -1:
            return "Permission Denied!(By discretionary access control rules)\n"
        # Remove \n from file_integ string
        file_integ = file_integ[:-1]
        file.close()

        if self._CheckMandatoryAccess(user_conf, user_integ, file_conf, file_integ) == -1:
            return "Permission Denied!(By mandatory access control rules)\n"

        # Begin read proccess
        file = open("Files/" + filename, "r")
        fileContent = file.readlines()
        file.close()
        return fileContent[2:]


    def _CheckDiscretionaryAccess(self, acl, username):
        index = acl.find(username + ':')
        if index == -1:
            return 1

        user_acl = acl[ index + len(username) + 1 : index + len(username) + 4]
        if 'r' in user_acl:
            return 1
        return -1

    # Check file's existance
    def _FileNameCheck (self, FileName):
        IsValid = -1
        dir = os.listdir('Files/')
        for names in dir :
            if FileName == names :
                IsValid = 1
        return IsValid

    def _CheckMandatoryAccess(self, user_conf, user_integ, file_conf, file_integ):
        # add a number to the beginning of level string
        user_conf = self._normalize_level(user_conf)
        user_integ = self._normalize_level(user_integ)
        file_conf = self._normalize_level(file_conf)
        file_integ = self._normalize_level(file_integ)

        if (user_conf >= file_conf and user_integ <= file_integ):
            return 1
        else:
            return -1

    def _normalize_level(self, level):
        # Add a number to the beginning of integ and 
        # conf level strings to make level comparison easier
        if (level == "TopSecret" or level == "VeryTrusted"):
            return "4" + level
        if (level == "Secret" or level == "Trusted"):
            return "3" + level
        if (level == "Confidential" or level == "SlightlyTrusted"):
            return "2" + level
        if (level == "Unclassified" or level == "Untrusted"):
            return "1" + level

