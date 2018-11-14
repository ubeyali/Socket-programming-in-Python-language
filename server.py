from socket import *
import threading

ip='192.168.1.8'

users = {}  # clients list for store client info
class Message:  # object to store message info
    def __init__(self, ip, port,userName,message,timestamp):
        self.userName = userName
        self.ip = ip
        self.port = port
        self.message=message
        self.timestamp=timestamp

    def prepMsg(self):  # prepare message to send it to other clients.
        msg=">>"+self.userName+"\n\t\t"+self.message+"\n"+"\t\t"+self.timestamp
        return msg
    def getMessage(self):   #return message string
        return (self.message)
    def getUsername(self):  # return client name
        return (self.userName)
    def getTimestamp(self): # return timestamp
        return (self.timestamp)

class User:
    def __init__(self, userName,ip,port):
        self.userName = userName
        self.ip=ip
        self.port=port

class ThreadedServer():
    def listenToClient(self, client, addr,user,name,port):
        clientConnected = True

        while clientConnected:
            message = client.recv(1024) # receive message from client
            recievedmessage1 = message.decode("utf-8")

            if 'exit' in (recievedmessage1):   # if it is 'exit' it will close the connection
                response = 'exiting from group..'
                client.send(response.encode('ascii'))
                users.pop(port)
                print(name + ' has been logged out from group')
                clientConnected = False
            else:
                recievedmessage = message.decode("utf-8")
                recievedMessage= recievedmessage.split(',',3)   #split the message to three parts
                messageObj = Message(str(addr[0]),str(addr[1]),recievedMessage[0],recievedMessage[1],recievedMessage[2])# pass ip,port,username,message,timestamp to the object.
                for i, j in users.items():  # go throw all the users connected
                    if j !=user:    # if it is the same client that writes the message don't send him the message. Otherwise send.
                       j.send(messageObj.prepMsg().encode('ascii')) #prepare the message and send it.
                print(messageObj.getUsername(), "says:", messageObj.getMessage(),"at",messageObj.getTimestamp()) #print to the server the client's name, message and the datetime

    def __init__(self, serverPort):

        try:
            serverSocket = socket(AF_INET, SOCK_STREAM) #create socket

        except:

            print("Socket cannot be created!!!")
            exit(1)

        print("Socket is created...")

        try:
            serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        except:

            print("Socket cannot be used!!!")
            exit(1)

        print("Socket is being used...")

        try:
            serverSocket.bind((ip, serverPort))
        except:

            print("Binding cannot de done!!!")
            exit(1)

        print("Binding is done...")

        try:
            serverSocket.listen(2)
        except:

            print("Server cannot listen!!!")
            exit(1)

        print("The server is ready to receive")

        while True:

            connectionSocket, addr = serverSocket.accept()
            ip1, port = str(addr[0]), str(addr[1])
            userName = connectionSocket.recv(1024).decode('ascii')  # receive client name from client
            print(userName,"joined the group")  # write to server

            connectionSocket.send(('Welcome to the group '+userName).encode('ascii'))   #sending welcoming message to client.
            for i, j in users.items():  # go throw all the users connected
                j.send((userName + " joined the group").encode('ascii'))  # send joining message to other clients.

            if (connectionSocket not in users): # add client to list if not exists already.

                users[port] = connectionSocket
                threading.Thread(target=self.listenToClient, args=(connectionSocket,addr,users[port],userName,port,)).start()


if __name__ == "__main__":
    serverPort = 12016
    ThreadedServer(serverPort)



