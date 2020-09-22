#IMPORT modules
import socket
import os
import json


HEADER = 512
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
SERVER = "192.168.0.105"
ADDR = (SERVER,PORT)
CONNECTED = True
LOGIN_MOD = True
CREATE_ACC = True

#clearing screen
def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


class ServerComm:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect(ADDR)
        pass

    def send(self,msg):
        try:
            msg = msg.encode(FORMAT)
            msg_length = len(msg)
            print(msg_length)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            self.client.send(send_length)
            self.client.send(b''+msg)
            return True
        except Exception as e:
            print(e)
            

    def recv(self):

        msg_length=int(self.client.recv(HEADER).decode(FORMAT))
        msg = self.client.recv(msg_length).decode(FORMAT)
        # print(json.loads(msg))
        return json.loads(msg)


class TerminalBank:

    def __init__(self):
        self.server_obj = ServerComm()        

    
    def dashboard(self,data):
        
        print(f"{'#'*20} WELCOME TO TERMINAL BANK {'#'*20}\n\n\n")
        print(f"Hello {data['name']}")


    def login(self):
        clear()
        LOGIN_MOD = True
        while LOGIN_MOD:
            print(f"{'#'*20} LOGIN {'#'*20}\n\n\n")
            print("ENTER username and password or press q to quit\n")
            username = input("USERNAME -> ")
            if username.lower() == 'q':
                LOGIN_MOD = False
                break
            password = input("password -> ")
            if password.lower() == 'q':
                LOGIN_MOD = False
                break
            
            if username and password:
                data = {
                    "type":"login",
                    'username':username,
                    'password':password
                }
            data = json.dumps(data)
            #send data to server will code here...
            if self.server_obj.send(data):
                data = self.server_obj.recv()
                LOGIN_MOD = False


    def create_acc(self,err=None):
        clear()
        CREATE_ACC = True
        if err is not None:
            print(f"<<!! {err} !!>>")

        while CREATE_ACC:
            print(f"{'#'*20} CREATE ACCOUNT {'#'*20}\n\n\n")
            print("Fill up the required credentials or press q to quit\n")
            # FORM
            name = input("Full name -> ")
            if name.lower() == 'q':
                CREATE_ACC = False
                break
            username = input("username (provide a unique one consisting of numbers and letters) -> ")
            if username.lower() == 'q':
                CREATE_ACC = False
                break
            password = input("password (provide a unique one consisting of numbers and letters) -> ")
            if password.lower() == 'q':
                CREATE_ACC = False
                break
            conf_password = input("confirm password (should match password you provided) -> ")
            if conf_password.lower() == 'q':
                CREATE_ACC = False
                break   
            
            # VALIDATING AND SENDING FORM
            if username and (password == conf_password):
                data_to_send = {
                    "type":"create_acc",
                    'name': name,
                    'username':username,
                    'password':password
                }
                data = json.dumps(data_to_send)
                if self.server_obj.send(data):
                    data = self.server_obj.recv()
                    if data['error'] == None:
                        print(data['data'])
                        CREATE_ACC = False
                        self.login()
                    else:
                        print(data['error'])
                        self.create_acc(err="ERROR IN DATA VALIDATION CHECK PASSWORD AND USERNAME")
            else:
                CREATE_ACC = False
                self.create_acc(err="ERROR IN DATA VALIDATION CHECK PASSWORD AND USERNAME")
           


    def menu(self):
        clear()
        print(f"{'#'*20} WELCOME TO TERMINAL BANK {'#'*20}\n\n\n")
        print("-> PRESS '1' TO LOGIN\n-> PRESS '2' TO CREATE ACCOUNT\n-> PRESS 'Q' to exit\n")
        selected = input()
        if selected == '1':
            self.login()
        elif selected == '2':
            print("Initiate CREATE ACCOUNT module")
            self.create_acc()
        elif selected.lower() == 'q':
            global CONNECTED
            CONNECTED = False
            # send disconnect msg..
            self.server_obj.send(DISCONNECT_MSG)
            print("quiting..")

    def init(self):

        while CONNECTED:    
            self.menu()


def start():
    terminalbank_obj = TerminalBank()
    terminalbank_obj.init()


if __name__ == '__main__':

    start()