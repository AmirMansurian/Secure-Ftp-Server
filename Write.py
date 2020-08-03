import os
import Auditor
import re

class Write:
    def WriteToFile(self, username, args, user_conf, user_integ, Logger, IsHoneyPot):
        if IsHoneyPot == 1:
            self.dir = "Fake/Files/"
        else:
            self.dir = "Files/"
        filename = args[0]
        # Log and audit the command before preventing attacks
        try:
            file = open(self.dir + filename)
            file_owner, file_conf, file_integ = file.readline().split(' ')
            file_acl = file.readline()
            index = file_acl.find(username + ':')
            if index == -1:
                user_acl = 'No DAC'
            else:
                user_acl = file_acl[index + len(username) + 1: index + len(username) + 4]

            file_conf = self._normalize_level(file_conf)
            file_integ = self._normalize_level(file_integ.strip('\n'))
        except FileNotFoundError:
            file_conf = ''
            file_integ = ''
            user_acl = ''

        Logger.Read_Write_Auditor(username, self._normalize_level(user_conf),
                                  self._normalize_level(user_integ),
                                  filename,
                                  file_conf,
                                  file_integ, user_acl, 'write', IsHoneyPot)

        # Check for path traversal attack
        if '\\' in filename or '/' in filename:
            return "Invalid file name"

        content = args[1]
        if self._FileNameCheck(filename) == -1:
            return "File Not Found !!!\n"

        # Read access control data from the file
        file = open(self.dir + filename, "r")
        file_header = file.readline()
        file_acl = file.readline()
        file_owner, file_conf, file_integ = file_header.split(' ')

        # 0 = no DAC, 1 = has the right, -1 = doesn't have the right
        DAC = self._CheckDiscretionaryAccess(file_acl, username)
        if DAC == -1:
            return "Permission Denied!(By discretionary access control rules)\n"
        elif DAC == 1:
            file.close()
            # Begin writing proccess
            file = open(self.dir + filename, "w")
            content = [file_header, file_acl, content]
            file.writelines(content)
            file.close()
            return "Writing on " + filename + " finished successfully."

        # Remove \n from file_integ string
        file_integ = file_integ[:-1]
        file.close()

        if self._CheckMandatoryAccess(user_conf, user_integ, file_conf, file_integ) == -1:
            return "Permission Denied!(By mandatory access control rules)\n"

        # Begin writing proccess
        file = open(self.dir + filename, "w")
        content = [file_header, file_acl, content]
        file.writelines(content)
        file.close()
        return "Writing on " + filename + " finished successfully."

    def _CheckDiscretionaryAccess(self, acl, username):
        index = acl.find(username + ':')
        if index == -1:
            return 0

        user_acl = acl[index + len(username) + 1: index + len(username) + 4]
        if 'w' in user_acl:
            return 1
        return -1

    # Check file's existance
    def _FileNameCheck(self, FileName):
        IsValid = -1
        dir = os.listdir(self.dir)
        for names in dir:
            if FileName == names:
                IsValid = 1
        return IsValid

    def _CheckMandatoryAccess(self, user_conf, user_integ, file_conf, file_integ):
        # add a number to the beginning of level string
        user_conf = self._normalize_level(user_conf)
        user_integ = self._normalize_level(user_integ)
        file_conf = self._normalize_level(file_conf)
        file_integ = self._normalize_level(file_integ)

        if (user_conf <= file_conf and user_integ >= file_integ):
            return 1
        else:
            return -1

    def _normalize_level(self, level):
        # Add a number to the beginning of integ and
        # conf level strings to make level comparison easier
        if (re.match(r'TopSecret', level, re.I) == None or re.match(r'VeryTrusted', level, re.I) == None):
            return "4" + level
        if (re.match(r'Secret', level, re.I) == None or re.match(r'Trusted', level, re.I) == None):
            return "3" + level
        if (re.match(r'Confidential', level, re.I) == None or re.match(r'SlightlyTrusted', level, re.I) == None):
            return "2" + level
        if (re.match(r'Unclassified', level, re.I) == None or re.match(r'Untrusted', level, re.I) == None):
            return "1" + level
