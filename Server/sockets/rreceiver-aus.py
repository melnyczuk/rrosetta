import socket, subprocess, os, time            # Import socket module
# import thread

def listen():
    while True:
        try:
            ear = socket.socket()         # Create a socket object
            host = "192.168.20.4"# socket.gethostbyname(socket.gethostname()) # Get local machine name
            port = 55345                 # Reserve a port for your service.
            ear.bind((host, port))        # Bind to the port
            print(ear.getsockname())
            ear.listen(10)                 # Now wait for client connection.
            print("listening...")
            c, addr = ear.accept()
            f = open('print.pdf','wb')
            while True:
                print('Got connection from', addr)
                print("Receiving..")
                l = c.recv(1024)
                while (l):
                    print("Receiving...")
                    f.write(l)
                    l = c.recv(1024)
                f.close()
                print("Done Receiving")
                c.close()                # Close the connections
            ear.close()
            listen()
        except Exception as e:
            print(e)
            pass
    listen()

if __name__ == "__main__":
    listen()