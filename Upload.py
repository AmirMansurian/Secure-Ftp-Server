import re
import os

class Upload :

    def PutFile (self ,Args) :

        Owner = Args[0];
        FileName = Args[1];
        ConfLevel = Args[2];
        IntegLevel = Args[3];

        if (self.FileNameCheck(FileName) == -1) :
            return "This file is already available\n"
        if re.match(r'TopSecret', ConfLevel, re.I) == None and re.match(r'Secret', ConfLevel, re.I) == None and re.match(r'Confidential', ConfLevel, re.I) == None and re.match(r'Unclassified', ConfLevel, re.I) == None :
            return "Confidentiality level is not Valid !!!\n"

        if re.match(r'VeryTrusted', IntegLevel, re.I) == None and re.match(r'Trusted', IntegLevel,re.I) == None and re.match(r'SlightlyTrusted',IntegLevel,re.I) == None and re.match(r'Untrusted', IntegLevel, re.I) == None:
                return "Integrity level is not Valid !!!\n"

        File = open("Files/" + FileName + ".txt", "w+\n")
        File.write(Owner + " " + ConfLevel + " " + IntegLevel)
        File.close()

        return FileName + ".txt" + " was successfully uploaded !!!\n"



    def FileNameCheck (self, FileName) :
        dir = os.listdir('Files/')
        for names in dir :
            if FileName + ".txt" == names :
                return -1
        return 1