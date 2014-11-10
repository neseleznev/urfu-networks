#!/usr/bin/env python
# -*- coding: 1251 -*-
import socket
import subprocess
import sys
import errno
from datetime import datetime
import threading

N_THREADS = 1000
TIMEOUT = 0.2


def cls():
	"Очистить экран"
	if sys.platform == 'win32':
		subprocess.call('cls', shell=True)
	else:
		subprocess.call('clear', shell=True)


def sexy_input():
	"Inputs remote server, returns it's IP"

	# Compability between python 2.x and 3.x
	try:
		input = raw_input
	except NameError:
		from builtins import input

	remoteServer    = input("Enter a remote host to scan: ")
	remoteServerIP  = socket.gethostbyname(remoteServer)

	# User-friendly interface ^^
	sys.stdout.write("\n")
	sys.stdout.write(("-" * 60) + "\n")
	sys.stdout.write("Please wait, scanning remote host " + remoteServerIP)
	if remoteServer != remoteServerIP:
		sys.stdout.write(" (" + remoteServer + ")")
	sys.stdout.write("\n")
	sys.stdout.write(("-" * 60) + "\n")

	return remoteServerIP


class ThScanner(threading.Thread):

    error_dict = errno.errorcode
    error_dict[0] = "(: Open :)"

    def __init__(self, sHost, iPort):
        threading.Thread.__init__(self)
        self.sHost = sHost
        self.iPort = iPort
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(TIMEOUT)
        self.udp_sock.settimeout(TIMEOUT)
 
    def run(self):        
        try:
            result = self.sock.connect_ex((self.sHost, self.iPort))
            if result == 0:
                print("Port {}: \t {}".format(self.iPort, self.error_dict[result]))
            # else:
            #     print("Port {}: \t {}".format(self.iPort, self.error_dict[result]))

            # self.udp_sock.connect_ex((self.sHost, self.iPort))
            # try:
            #     self.udp_sock.recv(10)
            # except socket.timeout:
            #     print("Port {} (udp): \t open".format(self.iPort))

        except KeyboardInterrupt:
            print("Program terminated by user")
            sys.exit(0)

        except socket.gaierror:
            print ("Hostname could not be resolved. Exiting")
            sys.exit(1)

        except socket.error:
            print("Couldn't connect to server")
            sys.exit(1)

        finally:      
            self.sock.close()
            self.udp_sock.close()


def scan(remoteServerIP, _range):
    try:
    	port = _range[0]
        while port in _range:
            if threading.activeCount() < N_THREADS :
                ThScanner(remoteServerIP, port).start()
                port += 1

    except KeyboardInterrupt:
        print("Program terminated by user")
        sys.exit(0)


def main():
	cls()
	remoteServerIP = sexy_input()

	# start_time = datetime.now()
	scan(remoteServerIP, range(1, 2 ** 16))
	# finish_time = datetime.now()
	# sys.stdout.write("Scanning Completed in " + str(finish_time - start_time))


if __name__ == "__main__":
	main()
