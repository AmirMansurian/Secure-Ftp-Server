import re
import os

class Upload :

    def PutFile (self ,Args, Owner, logger, IsHoneyPot) :

        FileName = Args[0];
        ConfLevel = Args[1];
        IntegLevel = Args[2];

        log = logger.Put_Get_Audit(Owner, FileName, "Put", IsHoneyPot)
        if log == -1 :
            return "You hade too many attemps for put file !!! \n"

        path = ""
        if IsHoneyPot == 0  :
            self.dir = "Files/"
        else :
            self.dir = "Fake/Files/"

        # Check for path traversal attack
        if '\\' in FileName or '/' in FileName:
            return "Invalid file name\n"

        if self.FileNameCheck(FileName) == -1 :
            return "This file is already available\n"
        if re.match(r'TopSecret', ConfLevel, re.I) == None and re.match(r'Secret', ConfLevel, re.I) == None and re.match(r'Confidential', ConfLevel, re.I) == None and re.match(r'Unclassified', ConfLevel, re.I) == None :
            return "Confidentiality level is not Valid !!!\n"

        if re.match(r'VeryTrusted', IntegLevel, re.I) == None and re.match(r'Trusted', IntegLevel,re.I) == None and re.match(r'SlightlyTrusted',IntegLevel,re.I) == None and re.match(r'Untrusted', IntegLevel, re.I) == None:
                return "Integrity level is not Valid !!!\n"

        if self.IntegCheck(Owner, IntegLevel) == -1 :
            return "You can not Put Files With Integrity level more than Your's !!!\n"

        File = open(self.dir + FileName, "w+")
        File.write(Owner + " " + ConfLevel + " " + IntegLevel + "\n")
        File.close()

        return FileName + " was successfully uploaded !!!\n"



    def FileNameCheck (self, FileName) :

        dir = os.listdir(self.dir)

        for names in dir :
            if FileName == names :
                return -1
        return 1

    def IntegCheck(self, Owner, IntegLevel):

        File = open("Users.txt", "r")
        Line = File.readlines()

        for line in Line :
            set = line.split(";")
            if set[0] == Owner :
                if self._normalize_level(set[2]) >= IntegLevel :
                    return 1
                else :
                    return -1
        return -1



    def _normalize_level(self, level):
        # Add a number to the beginning of integ and
        # conf level strings to make level comparison easier
        if (re.match(r'TopSecret', level, re.I) == None or re.match(r'VeryTrusted', level, re.I) == None):
                return "4"
        if (re.match(r'Secret', level, re.I) == None or re.match(r'Trusted', level, re.I) == None):
                return "3"
        if (re.match(r'Confidential', level, re.I) == None or re.match(r'SlightlyTrusted', level, re.I) == None):
                return "2"
        if (re.match(r'Unclassified', level, re.I) == None or re.match(r'Untrusted', level, re.I) == None):
                return "1"