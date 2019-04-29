alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 
            'w', 'x', 'y', 'z', 'unknown']



class Registration():

    account_name = ""
    account_id = ""
    account_pass = ""
    account_pass_re = ""
    account_email = ""
    path = ""
    ERROR_MESSAGE = ""


    def __init__(self, name, id, password, password_re, email):
        self.account_name = name
        self.account_id = id
        self.account_pass = password
        self.account_pass_re = password_re
        self.account_email = email

        if self.ERROR_MESSAGE == "":
            self.check_details_authenticity()

        if self.ERROR_MESSAGE == "":
            self.check_registration()

        if self.ERROR_MESSAGE == "":
            self.register()



    def register(self):
        write_file = open(self.path, "a")

        write_file.write('{} {} {} {} \n'.format(self.account_name,
                                              self.account_id,
                                              self.account_pass,
                                              self.account_email))

        write_file.close()



    def check_registration(self):
        for letter in alphabet:
            aux_path = "db/accounts/" + letter
            line = []

            with open(aux_path) as read_file:
                for each_line in read_file:
                    if not each_line == "":
                        line.append(each_line)
                    else:
                        break

            if line:
                line = [remove_endline.strip() for remove_endline in line]

                for account in line:
                    each_element = []
                    each_element = account.split()

                    #validating the name
                    if self.account_name == each_element[0]:
                        self.ERROR_MESSAGE = "Name already in use"
                        return

                    #validating the id
                    if self.account_id == each_element[1]:
                        self.ERROR_MESSAGE = "Id already in use"
                        return

                    #validating the password
                    if self.account_pass == each_element[2]:
                        self.ERROR_MESSAGE = "Please add a more secure password"
                        return

                    #validating the email
                    if self.account_email == each_element[3]:
                        self.ERROR_MESSAGE = "Email already in use"
                        return



    def check_details_authenticity(self):
        if(self.account_name == "" or
           self.account_id == "" or
           self.account_pass == "" or
           self.account_pass_re == "" or
           self.account_email == ""):
            self.ERROR_MESSAGE = "Please fill in all the fields!"
            return

        if not self.account_pass == self.account_pass_re:
            self.ERROR_MESSAGE = "Passwords don't match!"
            return

        #validating the name
        if len(self.account_name) < 2:
            self.ERROR_MESSAGE = "Please add a real name"
            return

        if len(self.account_name.split()) > 1:
            self.ERROR_MESSAGE = "Please don't use spaces"
            return
        #end name

        #validating the id
        if len(self.account_id) < 5:
            self.ERROR_MESSAGE = "Please insert a 6 characters long ID"
            return

        if len(self.account_id.split()) > 1:
            self.ERROR_MESSAGE = "Please don't use spaces"
            return
        #end id

        #validating the password
        if len(self.account_pass) < 7:
            self.ERROR_MESSAGE = "Please insert a 8 characters long Password"
            return

        if len(self.account_pass.split()) > 1:
            self.ERROR_MESSAGE = "Please don't use spaces"
            return
        #end password

        #validating the email
        if len(self.account_email.split()) > 1:
            self.ERROR_MESSAGE = "Please don't use spaces"
            return
        #end email

        characters_array = list(self.account_id)
        for char in alphabet:
            if characters_array[0].lower() == char:
                self.path = "db/accounts/" + char
                return
        self.path = "db/accounts/unknown"



    def __del__(self):
        account_name = ""
        account_id = ""
        account_pass = ""
        account_pass_re = ""
        account_email = ""
        path = ""
        ERROR_MESSAGE = ""









class Login():

    account_id = ""
    account_pass = ""
    path = ""
    ERROR_MESSAGE = ""



    def __init__(self, id, password):
        self.account_id = id
        self.account_pass = password

        if self.ERROR_MESSAGE == "":
            self.get_path()

        if self.ERROR_MESSAGE == "":
            self.check_account_exists()

        if self.ERROR_MESSAGE == "":
            self.user_login()



    def get_path(self):
        if(self.account_id == "" or
           self.account_pass == ""):
            self.ERROR_MESSAGE = "Please fill in all the fields"
            return

        characters_array = list(self.account_id)
        for char in alphabet:
            if characters_array[0].lower() == char:
                self.path = "db/accounts/" + char
                return
        self.path = "db/accounts/unknown"




    def check_account_exists(self):
        line = []

        with open(self.path) as read_file:
            for each_line in read_file:
                if not each_line == "":
                    line.append(each_line)
                else:
                    break

        if line:
            self.ERROR_MESSAGE = "You are not registered or the details are wrong!"
            line = [remove_endline.strip() for remove_endline in line]

            for account in line:
                each_element = []
                each_element = account.split()

                if(self.account_id == each_element[1] and
                   self.account_pass == each_element[2]):
                    self.ERROR_MESSAGE = ""
                    return
        else:
            self.ERROR_MESSAGE = "You are not registered or the details are wrong!"



    def user_login(self):
        self.ERROR_MESSAGE = ""



    def __del__(self):
        account_id = ""
        account_pass = ""
        path = ""
        ERROR_MESSAGE = ""








    path = "db/accounts/"


    def __enter__(self):
        characters_array = list(self.account_id)
        self.path += characters_array[0].lower()

        with open(self.path) as read_file:
            for each_line in read_file:
                self.line.append(each_line)

        self.line = [remove_endline.strip() for remove_endline in self.line]
        self.line = self.line[0].split()

        return self





#name = raw_input("Name: ")
#id = raw_input("ID: ")
#password = raw_input("Password: ")
#pass_re = raw_input("Confirm password: ")
#email = raw_input("Email: ")

#test = Registration(name, id, password, pass_re, email)



#id = raw_input("ID: ")
#password = raw_input("Password: ")

#test = Login(id, password)

#if not test.ERROR_MESSAGE == "":
#    print(test.ERROR_MESSAGE)




#id = raw_input("ID: ")

#test = Navigate(id)

#print(test.line)
