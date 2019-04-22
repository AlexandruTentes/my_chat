import socket
import threading
import sys

IP = '127.0.0.1'
PORT = 22000
bytes_amount_per_message = 1024

class Client:

    TCP_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_IP = IP
    server_PORT = PORT
    data_size = bytes_amount_per_message
    received_message = ''
    ERROR_MESSAGE = ''



    def __init__(self): 
        try:
            self.TCP_server_socket.connect((self.server_IP, self.server_PORT))
        except:
            self.close_connection("Cannot connect to the server")
            return

        recv_message_thread = threading.Thread(target = self.msg_handler_recv)
        recv_message_thread.daemon = True
        recv_message_thread.start()
    
    

    def close_connection(self, message):
        self.TCP_server_socket.close()
        self.ERROR_MESSAGE = message



    def send_message(self, message):
        try:
            self.TCP_server_socket.send(bytes(message, 'UTF-8'))
        
        except:
            self.close_connection("Connection has unexpectedly closed")
            return



    def get_message(self):
        return self.received_message
        


    def msg_handler_recv(self):
        while True:
            try:
                data = self.TCP_server_socket.recv(self.data_size)              
                
                self.received_message = str(data, 'utf-8')

            except ConnectionResetError:
                self.close_connection("Connection has unexpectedly closed")
                return

            except:
                self.close_connection("Closing the program")
                return



client = Client()

def test():
    while True:
        if not client.get_message() == '':
            print(client.get_message())
            client.received_message = ''

        if not client.ERROR_MESSAGE == '':
            print(client.ERROR_MESSAGE)
            break

t = threading.Thread(target=test)
t.daemon = True
t.start()

while True:
    if not client.ERROR_MESSAGE == '':
        break

    client.send_message(input(""))

