import socket
import threading

class chatserver:
    def __init__(self,host="localhost" ,port=9999):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host,self.port))
        self.server.listen()
        self.client = []
        self.nicknames = []
    def broadcast(self,message):
        for client in self.clients:
            client.send(message)

    def handle(self,client):
        while True:
            try:
                message =  client.recv(1024)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.client.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                self.broadcast(f"{nickname} left the chat!".encode("ascii"))
                break
    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")

            client.send("Nick".encode("ascii"))
            nickname = client.recv( 1024).decode(ascii)
            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f"Nickname of the client is {nickname}!")
            self.broadcast(f"{nickname} joinded the chat!".encode("ascii"))
            client.send("Connected to the server!".encode("ascii"))

            thread = threading.Thread(target=self.handle,args=(client,))
            thread.start()
    
    def run(self):
        print("Server Started!")
        self.receive()
if __name__ == "__main__":
    chatserver().run()
        

        
