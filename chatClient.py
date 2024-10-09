import socket
import threading
import tkinter as tk

class ChatClient:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, self.port))
        except ConnectionRefusedError:
            print("Connection refused. Is the server running?")
            return
        except socket.gaierror:
            print("Invalid host or port. Please check the host and port.")
            return
        except Exception as e:
            print(f"An error occurred: {e}")
            return

        self.nickname = input("Choose a nickname: ")
        self.client.send(self.nickname.encode('ascii'))

        self.root = tk.Tk()
        self.root.title("Chat Client")

        self.text_area = tk.Text(self.root)
        self.text_area.pack(padx=10, pady=10)

        self.entry = tk.Entry(self.root)
        self.entry.pack(padx=10, pady=10)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('ascii'))
                else:
                    self.text_area.insert(tk.END, message + "\n")
            except ConnectionResetError:
                print("Connection reset. The server may have closed the connection.")
                self.client.close()
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                self.client.close()
                break

    def send_message(self):
        message = self.entry.get()
        if message == "/quit":
            self.client.close()
            self.root.quit()
        message = f'{self.nickname}: {message}'
        self.client.send(message.encode('ascii'))
        self.entry.delete(0, tk.END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ChatClient().run()