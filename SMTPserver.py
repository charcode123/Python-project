import socket, threading
import json
import user_authentication as ua
import user_validity as uv
import mail_handler as mh
import registration as reg
def receive_json(conn):
    data = conn.recv(4096)
    data = data.decode('utf-8')
    data = json.loads(data)
    return data
def receive_data(conn):
    data = conn.recv(4096)
    data = data.decode('utf-8')
    return data    
class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
        self.csocket.send(bytes("Connection estblished",'UTF-8'))
    def run(self):
        while True:
            data=receive_json(self.csocket)
            if data["choice"]=="1":
                username=data['username']
                password=data['password']
                x=ua.user_auth(username,password)
                if x==True:
                    self.csocket.send(bytes("True","UTF-8"))
                else:
                    self.csocket.send(bytes("False","UTF-8"))
                    continue
                while True:
                    choice=receive_data(self.csocket)
                    if choice=="1":
                        self.csocket.send(bytes("COMPOSE","UTF-8"))
                        to=receive_data(self.csocket)
                        print(to)
                        x=uv.user_validity(to)
                        if x==True:
                            self.csocket.send(bytes("True","UTF-8"))
                        else:
                            self.csocket.send(bytes("False","UTF-8"))
                            continue      
                        data=receive_json(self.csocket)
                        x=mh.send_mail(data)
                        self.csocket.send(bytes("Mail sent successfully","UTF-8"))
                    elif choice=="2":
                        x=mh.view_inbox(username)
                        print(x)
                        self.csocket.send(bytes(x,"UTF-8"))
                    elif choice=="3":
                        x=mh.view_sent(username)
                        print(x)
                        self.csocket.send(bytes(x,"UTF-8"))
                    elif choice=="4":
                        print ("Client at ", clientAddress , " disconnected...")
                        self.csocket.send(bytes("Logged out","UTF-8"))
                        break        
            if data["choice"]=="2":
                x=reg.user_registration(data['username'],data['password'])
                if x==True:
                    self.csocket.send(bytes("True","UTF-8"))
                else:
                    self.csocket.send(bytes("False","UTF-8"))
            if data["choice"]=="3":
                print ("Client at ", clientAddress , " disconnected...")
                break            


        
LOCALHOST = "127.0.0.1"
PORT = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(2)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()