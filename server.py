#IMPORT MODULES
import socket
import threading
import json
import os
import signal

#CONSTANTS
PORT = 5050
SERVER = socket.gethostbyname_ex(socket.gethostname())[-1][-1] #get the ip address
ADDR = (SERVER,PORT)
CONNECTED = True
THREAD_COUNT = 0
HEADER = 512
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
LOGGED_IN = []

class TerminalBankServer:

    def create_acc(self,data):
        print(data)
        # code here....
        try:
            if os.path.exists(f"./db/_{data['username']}.json"):
                return {'status':False,'data': None,"error":"username already exists.."}

            with open(f"db/_{data['username']}.json",'w') as f:
                del data['type']
                data['balance'] = 0.0
                json.dump(data,f)
            return {'status': True,'data': data,"error":None}
        except Exception as e:
            print(e)
            return {'status':False,'data': None,"error":"something went wrong.."}

    def login(self,data):
        print(data['username'],data['password'])

        try:
            if os.path.exists(f"./db/_{data['username']}.json"):
                print("exists")
                with open(f"./db/_{data['username']}.json",'r') as f:
                    data_from_file = json.load(f)
                    if data_from_file['password'] == data['password']:
                        print("password correct")
                        if data['username'] not in LOGGED_IN:
                            LOGGED_IN.append(data['username'])
                        
                        return {'status':True,'data':data_from_file,'error':None}
            return {'status':False,'data':None,'error':"username does not exists.."}
        except Exception as e:
            print(e)
            return {'status':False,'data':None,'error':e}

    def category(self,type):
        if type == 'login':
            return self.login
        elif type == 'create_acc':
            return self.create_acc


def client_handle(conn,addr):
    print(f"[NEW CONNECTION] from {addr}")
    client_connected = True
    server_obj = TerminalBankServer()
    while client_connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            # print(msg_length)
            if msg_length:
                msg_length = int(msg_length)
                try:
                    msg = conn.recv(msg_length).decode(FORMAT)
                    print(f"[{addr}] {msg}")
                    data = json.loads(msg)
                    returned_func = server_obj.category(data['type'])
                    result = returned_func(data)
                    msg = json.dumps(result)
                    msg_length = len(msg)
                    conn.send(bytes(str(HEADER - msg_length),FORMAT))
                    conn.send(bytes(msg,FORMAT))
                except Exception as e:
                    print(e)
                
                # msg_server = "message received..."
                # msg_length = len(msg)
                # conn.send(bytes(str(HEADER - msg_length),FORMAT))
                # conn.send(bytes(msg_server,FORMAT))
                if msg == DISCONNECT_MSG:
                    client_connected = False
            # else:
            #     client_connected = False
        except Exception as e:
            print(e)
            client_connected = False
            conn.close()
    conn.close()


def start():
    """
    This is the function which is going to start the server to listen on port 5050 
    for incoming steams from clients
    """
    #creating socket object
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #binding the server to an address
    server.bind(ADDR)
    server.listen()
    print("[ACTIVE] Server listening on port 5050...")

    #for multiple client connections
    while CONNECTED:
        try:
            conn,addr = server.accept()
            #passing each client conneciton to a thread
            thread = threading.Thread(target=client_handle,args=(conn,addr))
            #starting the thread
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        except KeyboardInterrupt:
            print("After interrupt...")
        

if __name__ == '__main__':
    start()