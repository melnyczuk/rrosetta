import socket
import os
import subprocess
import time


def listen():
    s = socket.socket()
    s.settimeout(3600)
    print("waiting...")
    s.connect(('218.214.105.53', 56456))
    s.settimeout(None)
    print("listen...")
    f = open('print.pdf', 'wb')
    l = s.recv(1024)
    while (l):
        print("hark!")
        f.write(l)
        l = s.recv(1024)
    f.close()
    s.close()
    if os.path.exists("print.pdf"):
        take_note()


def take_note():
    print("a zine is born!")
    # osx
    os.startfile("print.pdf", "print")
    # subprocess.run(["/usr/bin/lpr", "-o portrait",
#                "-o media=A4", "-o number-up=2", "print.pdf"])

    os.remove("print.pdf")
    listen()


if __name__ == "__main__":
    listen()
