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
LOGGED_IN = False
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
            # print(msg_length)
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
        global LOGGED_IN
        if LOGGED_IN:
            # clear()
            # print(f"{'#'*20} WELCOME TO TERMINAL BANK {'#'*20}\n\n\n")
            # print(f"Hello {data['data']['name']}")
            DASHBOARD_MOD = True
            while DASHBOARD_MOD:
                clear()
                print(f"{'#'*20} WELCOME TO TERMINAL BANK {'#'*20}\n\n\n")
                print(f"Hello {data['data']['name'].upper()}")
                selected = input("\n-> PRESS 1 TO CHECK BALANCE\n-> PRESS 2 TO WITHDRAW MONEY\n-> PRESS 3 TO ADD MONEY\n-> PRESS L TO LOGOUT\n\n")
                # print(selected)
                if selected.lower() == 'l':
                    LOGGED_IN = False
                    DASHBOARD_MOD = False
                
                elif selected == '1':
                    print(f"your balance is {data['data']['balance']}")
                    _ = input("press ENTER")
                
                elif selected == '2':
                    amount_to_withdraw = input("amount to withdraw -> ")
                    if float(amount_to_withdraw) < float(data['data']['balance']):
                        data_to_send = json.dumps({
                            "type":"withdraw_money",
                            "username": data['data']['username'],
                            "amount_to_withdraw" : amount_to_withdraw
                        })
                        #server call to save
                        if self.server_obj.send(data_to_send):
                            returned_data = self.server_obj.recv()
                            if returned_data['status']:
                                data['data']['balance'] = float(data['data']['balance']) - float(amount_to_withdraw)
                                print(f"amount of {amount_to_withdraw} is withdrawn")
                                print(f"New Balance -> {data['data']['balance']}")
                            else:
                                print(data['error'])
                        _ = input("press ENTER")
                    else:
                        print("insufficient balance for withdrawl")
                        _ = input("press ENTER")
                
                elif selected == '3':
                    amount_to_add = input("amount to add -> ")
                    data_to_send = json.dumps({
                        "type":"add_money",
                        "username":data['data']['username'],
                        "amount_to_add" : amount_to_add
                    })
                    #server call to save
                    if self.server_obj.send(data_to_send):
                        returned_data = self.server_obj.recv()
                        if returned_data['status']:
                            data['data']['balance'] = float(data['data']['balance'] + float(amount_to_add))
                            print(f"New Balance -> {data['data']['balance']}")          
                        else:
                            print(returned_data['error'])
                    _ = input("press ENTER")

                elif selected == '4':

                    #server call to delete account

                    # temp_data = {}
                    # for key,val in data['data'].items():
                    #     if key != 'balance' and key != 'username':
                    #         if key != 'password':
                    #             print(f"{key} -> {val}")
                    #             user_input = input(f"{key} [press 's' to skip] -> ")
                    #             if user_input == 's':
                    #                 continue
                    #             else:
                    #                 temp_data[key] = user_input
                    #         else:
                    #             print(f"{key} -> ********")
                    #             user_input = input(f"{key} [press 's' to skip] -> ")
                    #             if user_input == 's':
                    #                 continue                           
                    #             conf_pass = input(f"confirm password [press 's' to skip] -> ")
                    #             if user_input == 's':
                    #                 continue
                    #             elif conf_pass == user_input:
                    #                 temp_data[key] = user_input
                    
                    # print(temp_data)
                    
                    #call to backend to save data

        else:
            self.login()


    def login(self,err=None):
        LOGIN_MOD = True
        while LOGIN_MOD:
            clear()
            if err is not None:
                print(f"!!!{err}!!!")
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
                if self.server_obj.send(data):
                    data = self.server_obj.recv()
                    if data['status']:
                        LOGIN_MOD = False
                        global LOGGED_IN
                        LOGGED_IN = True
                        self.dashboard(data=data)
                    else:
                        LOGIN_MOD = False
                        self.login(err=data['error'])


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