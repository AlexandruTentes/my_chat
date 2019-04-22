import socket
import threading

IP = '127.0.0.1'
PORT = 22000
bytes_amount_per_message = 1024

class Server:

    TCP_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_IP = IP
    server_PORT = PORT
    sockets_connected_list = []
    data_size = bytes_amount_per_message



    def __init__(self): 
        self.TCP_server_socket.bind((self.server_IP, self.server_PORT))
        self.TCP_server_socket.listen()



    def each_connection_handler(self, connection, address):
        while True:
            try:
                socket_data = connection.recv(self.data_size)

                #still have to figure out the issue with handling client disconnection
                #=============#
                if len(socket_data) == 0:
                    print(str(address[0]), ' : ', str(address[1]), " --- disconnected")
                    self.sockets_connected_list.remove(connection)
                    connection.close()
                    break
                #=============#

                for each_socket in self.sockets_connected_list:
                    each_socket.send(socket_data)

            except:

                #only occurs if the package fails to be sent back to the client
                #which made the the request to receive the package
                #=============#
                print("Connection with the IP ", address[0],"abnormally intrerupted")
                print(str(address[0]), ' : ', str(address[1]), " --- disconnected")
                self.sockets_connected_list.remove(connection)
                connection.close()
                break
                #=============#



    def run_server(self):
        while True:
            connection_scoket, connection_scoket_address_IP = self.TCP_server_socket.accept() 
            
            connection_thread = threading.Thread(target=self.each_connection_handler, args=(connection_scoket, connection_scoket_address_IP))   
            connection_thread.daemon = True
            connection_thread.start()

            self.sockets_connected_list.append(connection_scoket)
            print(str(connection_scoket_address_IP[0]), ' : ', str(connection_scoket_address_IP[1]), " --- connected")



server = Server()
server.run_server()