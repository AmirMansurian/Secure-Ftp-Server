import os

class List :

    def GetList (self, arg, Username, ConfLevel, IsHoneyPot) :

        path =""
        if IsHoneyPot == 0 :
            self.dir = "Files/"
        else :
            self.dir = "Fake/Files/"

        dir = os.listdir(self.dir)
        Result = ""

        for file in dir :

            File = open(self.dir + file, "r")
            line = File.readline()
            if not line:
                break

            set = line.split(" ")
            if int((self._normalize_level(ConfLevel)[0]) >= self._normalize_level(set[1])[0]) or Username == set[0] :
                if arg in file :
                    Result += file + "      " + set[0] + "/" + set[1] + "/" + set[2] + "\n"
            File.close()

        return Result

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
