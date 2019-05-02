#included packages
import socket
import threading
import time

#custom database
import db
import db_functions

IP = '167.99.193.70'
PORT = 22000
bytes_amount_per_message = 1024
user_login_check = False

class Server:

    TCP_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_IP = IP
    server_PORT = PORT
    sockets_connected_list = {}
    sockets_connected_names = {}
    data_size = bytes_amount_per_message



    def __init__(self):
        try:
            #makes sure to re-use the freshly closed ports
            #still might throw the error
            self.TCP_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            #simply bind the server to the ip and port
            #and start listening
            self.TCP_server_socket.bind((self.server_IP, self.server_PORT))
            self.TCP_server_socket.listen(1)

        except:
            print("Error at starting the server. Check the IP and PORT!")
            return



    def each_connection_handler(self, connection, address):
        while True:
            try:
                socket_data = connection.recv(self.data_size)

                #still have to figure out the issue with handling client disconnection
                #=============#
                if len(socket_data) == 0:
                    print(str(address[0]), ' : ', str(address[1]), " --- disconnected")
                    del self.sockets_connected_list[(connection, address)]
                    connection.close()
                    break
                #=============#

                #=== handle the Auth ===
                #retrieving the very first word
                command_check = str(socket_data)
                command_check = command_check.split()

                if len(command_check) == 0:
                    command_check.append(" ")

                #checking if the first word is a command
                #checking if the user is already connected to lower the commands to be used

                user_command = False

                current_socket_data = self.sockets_connected_list.get((connection, address))
                current_socket_data[5] = 0
                self.sockets_connected_list.update(
                        {(connection, address) : current_socket_data})

                if command_check[0] == "@>":
                    if len(command_check) > 1:
                        user_command = switch_commands(command_check[1])
                        if user_command == False:
                            connection.send(bytes("===> Please enter a valid command <==="))
                        command_check.remove(command_check[0])
                    else:
                        connection.send(bytes("===> Please enter a valid command <==="))

                    if(user_command == "AUTH" and
                       self.sockets_connected_list.get((connection, address))[0] == False):
                        command_successful = execute_command(command_check, (connection, address))

                        #check if the command is for registration or login and handle them
                        if command_successful == True:
                            current_socket_data = self.sockets_connected_list.get((connection, address))
                            current_socket_data[0] = True
                            self.sockets_connected_list.update(
                                    {(connection, address) : current_socket_data})
                        else:
                            connection.send(bytes(command_successful))

                    elif(user_command == "DISC" and
                         self.sockets_connected_list.get((connection, address))[0] == True):
                        command_successful = execute_command(command_check, (connection, address))

                    elif(user_command == "PMSG" and
                         self.sockets_connected_list.get((connection, address))[0] == True):
                        command_successful = execute_command(command_check, (connection, address))

                        if not command_successful == True:
                            connection.send(bytes(command_successful))

                    elif(user_command == "GMSG" and
                         self.sockets_connected_list.get((connection, address))[0] == True):
                        command_successful = execute_command(command_check, (connection, address))


                    current_socket_data = self.sockets_connected_list.get((connection, address))
                    current_socket_data[5] = 1
                    self.sockets_connected_list.update(
                            {(connection, address) : current_socket_data})

                    user_command = True

                if self.sockets_connected_list.get((connection, address))[0] == True:
                    #this if condition deals with the message which specifies that the user
                    #has successfully connected
                    #It happens only once per login
                    if self.sockets_connected_list.get((connection, address))[1] == 0:
                        connection.send(bytes("{[|_CONNECTED_|]}"))
                        current_socket_data = self.sockets_connected_list.get((connection, address))
                        current_socket_data[1] = 1
                        self.sockets_connected_list.update(
                                {(connection, address) : current_socket_data})

                        #retireve the name from the database
                        current_socket_data = self.sockets_connected_list.get((connection, address))
                        nav_this_socket = db_functions.search_by_id(current_socket_data[2])

                        #check if the file exists in the db
                        if not nav_this_socket == False:
                            current_socket_data[3] = nav_this_socket[0]
                        del nav_this_socket

                        self.sockets_connected_list.update(
                                {(connection, address) : current_socket_data})
                        print(connection, ": has logged in with the details:",
                                self.sockets_connected_list.get((connection, address)))

                        #add the sockets by name as keys
                        self.sockets_connected_names.update(
                                {current_socket_data[3] : [connection, self.sockets_connected_list.get((connection, address))[0]]})

                    else:
                        for(each_socket, each_socket_data) in self.sockets_connected_list.items():
                            if each_socket_data[0] == True:
                                if self.sockets_connected_list.get((connection, address))[5] == 0:
                                    if self.sockets_connected_list.get((connection, address))[4] == "":
                                        modified_data = self.sockets_connected_list.get((connection, address))[3] + ": " + str(socket_data)
                                        each_socket[0].send(bytes(modified_data))
                                    else:
                                        modified_data = ">>> " + self.sockets_connected_list.get((connection, address))[3] + ": " + str(socket_data)
                                        connection.send(bytes(modified_data))
                                        if self.sockets_connected_names.get(self.sockets_connected_list.get((connection, address))[4])[1] == True:
                                            self.sockets_connected_names.get(self.sockets_connected_list.get((connection, address))[4])[0].send(bytes(modified_data))
                                        break

                else:
                    if user_command == False:
                        connection.send(bytes("===> Please login or register to send messages <==="))

            except:

                #only occurs if the package fails to be sent back to the client
                #which made the request to receive the package
                #=============#
                print("Connection with the IP ", address[0],"abnormally intrerupted")
                print(str(address[0]), ' : ', str(address[1]), " --- disconnected")
                del self.sockets_connected_list[(connection, address)]
                print("users left: " + str(len(self.sockets_connected_list)))
                connection.close()
                break
                #=============#



    def run_server(self):
        while True:
            connection_socket, connection_socket_address_IP = self.TCP_server_socket.accept()

            self.sockets_connected_list[(connection_socket, connection_socket_address_IP)] = [False, 0, "", "", "", 0]
            print(str(connection_socket_address_IP[0]), ' : ', str(connection_socket_address_IP[1]), " --- connected")

            connection_thread = threading.Thread(target=self.each_connection_handler, args=(connection_socket, connection_socket_address_IP))
            connection_thread.daemon = True
            connection_thread.start()

            try:
                connection_socket.send(bytes("To start using the commands type '@>' followed by a space and one of the following:"))
                time.sleep(.300)
                connection_socket.send(bytes("'register' - name id pass pass email"))
                time.sleep(.200)
                connection_socket.send(bytes("'login' - id pass"))
                time.sleep(.200)
                connection_socket.send(bytes("'message' - name : send private messages"))
                time.sleep(.200)
                connection_socket.send(bytes("'global' - *no arguments* : connect to global chat"))
                time.sleep(.200)
                connection_socket.send(bytes("'disconnect' - *no arguments* : log out of your account"))

            except:
                print("connection lost, client crash")



#========================
#=== Useful functions ===
#========================

#checking if the given patter is a command
def switch_commands(pattern):
    list = {
        "login": "AUTH",
        "register": "AUTH",
        "disconnect" : "DISC",
        "message" : "PMSG",
        "global" : "GMSG",
        "create_channel" : "CRCH",
        "join_channel" : "JOCH",
        "invite_channel" : "INCH",
        "delete_channel" : "DLCH"
    }

    return list.get(pattern, False)



#============================
#=== Handling the pattern ===
#============================

#executing the command
def execute_command(command, connection):
    if command[0] == "login":
        login = db.Login(command[1] if len(command) == 3 else "",
                         command[2] if len(command) == 3 else "")

        if not login.ERROR_MESSAGE == "":
            error = login.ERROR_MESSAGE
            del login
            return error

        current_socket_data = server.sockets_connected_list.get(connection)
        current_socket_data[2] = command[1]
        server.sockets_connected_list.update({connection : current_socket_data})
        del login

    elif command[0] == "register":
        register = db.Registration(command[1] if len(command) == 6 else "",
                                   command[2] if len(command) == 6 else "",
                                   command[3] if len(command) == 6 else "",
                                   command[4] if len(command) == 6 else "",
                                   command[5] if len(command) == 6 else "")

        if not register.ERROR_MESSAGE == "":
            error = register.ERROR_MESSAGE
            del register
            return error

        current_socket_data = server.sockets_connected_list.get(connection)
        current_socket_data[2] = command[2]
        server.sockets_connected_list.update({connection : current_socket_data})
        del register

    elif command[0] == "disconnect":
        current_socket_data = server.sockets_connected_list.get(connection)

        server.sockets_connected_names.update(
                {current_socket_data[3] : [connection[0], False]})

        current_socket_data[0] = False
        current_socket_data[1] = 0
        current_socket_data[2] = ""
        current_socket_data[3] = ""

        server.sockets_connected_list.update(
                {connection : current_socket_data})
        connection[0].send(bytes("{[|_DISCONNECTED_|]}"))

    elif command[0] == "message":
        other_socket_name = command[1] if len(command) == 2 else ""

        if other_socket_name == "":
            return "===> Please enter the person's name <==="

        if server.sockets_connected_names.get(other_socket_name):
            current_socket_data = server.sockets_connected_list.get(connection)
            current_socket_data[4] = other_socket_name
            server.sockets_connected_list.update({connection : current_socket_data})
            connection[0].send(bytes("{[|_MESSAGE_|]}" + str(other_socket_name)))
        else:
            return "===> Please add an existing user name <==="

    elif command[0] == "global":
        current_socket_data = server.sockets_connected_list.get(connection)
        current_socket_data[4] = ""
        server.sockets_connected_list.update({connection : current_socket_data})
        connection[0].send(bytes("===> Joining global chat <==="))

    return True


#initializing the server
server = Server()

#running the server
server.run_server()
