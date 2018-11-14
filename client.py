import datetime
import threading
import socket
serverName="192.168.1.8"
serverPort=12016
clientcheck=True
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #create sokcet object

userName=input("Enter your name: ") #request name from the client
clientSocket.connect((serverName,serverPort))   #connect to socket via ip and port
clientSocket.send(userName.encode())  #send userName to server
def recMsg(sock):
    while True :
        msg = sock.recv(1024).decode('ascii')   #receive data from server (messages from other clients and notificatoins from server)
        print(msg)

threading.Thread(target = recMsg, args = (clientSocket,)).start()
while clientcheck:
    message=input()
    dt=datetime.datetime.now()
    dateStr= dt.strftime('%Y-%m-%d %H:%M:%S')

    if message=="exit":
        clientcheck=False
        clientSocket.send('exit'.encode('ascii'))
        #clientSocket.close()
        exit(0)
    else:
        clientSocket.send((userName + "," + message + "," + dateStr).encode())  # send client info to server splitted by ','
