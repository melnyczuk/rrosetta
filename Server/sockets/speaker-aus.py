import socket, subprocess, os, time, datetime

def main():
    while True:
        try:
            make_connection()
        except Exception as e:
            print(e)
            pass

def make_connection():
    jaw = socket.socket()         # Create a socket object
    host = "192.168.20.4"# socket.gethostbyname(socket.gethostname()) # Get local machine name
    port = 56456                 # Reserve a port for your service.
    jaw.bind((host, port))        # Bind to the port
    print(jaw.getsockname())
    jaw.listen(10)
    print("heavy breathing...")
    if os.path.exists('print.pdf'):
        os.remove("print.pdf")  
    c, addr = jaw.accept()
    prepare(jaw, c, addr)
    

def prepare(jaw, c, addr):
    if os.path.exists('print.pdf'):
        speak(jaw, c, addr)
    else:
        print("waiting...")
        time.sleep(60)
        prepare(jaw, c, addr)

def speak(jaw, c, addr):
    print("Sending To:", addr)
    f = open('print.pdf','rb')
    l = f.read(1024)
    while (l):
        print("loud noises!")
        c.send(l)
        l = f.read(1024)
    f.close()
    os.remove("print.pdf")
    c.close()
    print("panting")
    jaw.close()
    jaw.shutdown(socket.SHUT_RDWR)
    make_connection()

if __name__ == "__main__":
    main()


