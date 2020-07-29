import os
class DACCommands():
    def GrantAccess(self, source_user, arg):
        permission = arg[0]
        filename = arg[1]
        target_user = arg[2] # The user gaining permission

        # Check for path traversal attack
        if '\\' in filename or '/' in filename:
            return "Invalid file name"
        
        # Check for file existance
        if self._FileNameCheck(filename) == -1:
            return "File Not Found !!!\n"

        # Check for target user existance
        if self._CheckUser(target_user) == -1:
            return "Username doesn't exist"
        
        # Read file's content and extract it's 
        # ownership and access control list 
        file = open("Files/" + filename, "r")
        content = file.readlines()
        file_owner = content[0].split(' ')[0]
        access_list = content[1]
        file.close()
        
        # Check ownership
        if file_owner != source_user:
            return "You can't grant access to this file because you are not the owner"

        # Create access permission rule
        new_permission = target_user + ':'
        if 'r' in permission:
            new_permission += 'r'
        else:
            new_permission += '-'
        if 'w' in permission:
            new_permission += 'w'
        else:
            new_permission += '-'
        if 'g' in permission:
            new_permission += 'g'
        else:
            new_permission += '-'

        new_permission += ';'

        # Update the ACL and write changes to the file
        self._UpdateAndWrite(access_list, target_user, new_permission, content, filename)
        return "Permission(s) granted successfully"


    def RevokeAccess(self, source_user, arg):
        permission = arg[0]
        filename = arg[1]
        target_user = arg[2] # The user losing permissions

        # Check for path traversal attack
        if '\\' in filename or '/' in filename:
            return "Invalid file name"
        
        # Check for file existance
        if self._FileNameCheck(filename) == -1:
            return "File Not Found !!!\n"

        # Check for target user existance
        if self._CheckUser(target_user) == -1:
            return "Username doesn't exist"

        # Read file's content and extract it's 
        # ownership and access control list 
        file = open("Files/" + filename, "r")
        content = file.readlines()
        file_owner = content[0].split(' ')[0]
        access_list = content[1]
        file.close()
        
        # Check ownership
        if file_owner != source_user:
            return "You can't revoke permissions to this file because you are not the owner"

        # Find user's access list index (position)
        user_access_index = access_list.find(target_user + ':')
        if (user_access_index == -1):
            return "The user has no permissions to be revoked"

        # Find target's rwg permissions 
        target_user_acl = access_list[user_access_index + len(target_user) + 1: user_access_index + len(target_user) + 4]

        # Create access permission rule
        new_permission = target_user + ':'
        if 'r' in permission:
            new_permission += '-'
        else:
            new_permission += target_user_acl[0]
        if 'w' in permission:
            new_permission += '-'
        else:
            new_permission += target_user_acl[1]
        if 'g' in permission:
            new_permission += '-'
        else:
            new_permission += target_user_acl[2]

        new_permission += ';'

        # Update the ACL and write changes to the file
        self._UpdateAndWrite(access_list, target_user, new_permission, content, filename)
        return "Permission(s) revoked successfully"


    def _UpdateAndWrite(self, access_list, target_user, new_permission, content, filename):
        # Find user's access list index (position)
        user_access_index = access_list.find(target_user + ':')
        
        # If the user has no pervious ACL record
        if user_access_index == -1:
            access_list = new_permission + access_list
        else:
            access_list = access_list[:user_access_index] + new_permission + access_list[len(new_permission) + user_access_index:] 
        
        content[1] = access_list

        # Write changes to the file
        file = open("Files/" + filename, "w")
        file.writelines(content)
        file.close()


    def _FileNameCheck (self, FileName):
        IsValid = -1
        dir = os.listdir('Files/')
        for names in dir :
            if FileName == names :
                IsValid = 1
        return IsValid


    def _CheckUser (self, username):
        file = open("Users.txt", 'r')
        
        lines = file.readlines()
        for line in lines:
            user = line.split(";")[0]
            if (user == username):
                return 1
        return -1
