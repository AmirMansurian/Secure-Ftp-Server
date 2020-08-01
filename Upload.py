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