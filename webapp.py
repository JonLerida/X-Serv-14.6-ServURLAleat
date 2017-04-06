#! /usr/bin/python3
"""
webApp class
 Root for hierarchy of classes implementing web applications
 Copyright Jesus M. Gonzalez-Barahona and Gregorio Robles (2009-2015)
 jgb @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - February 2015
"""

import socket
import random


class webApp:
    """Root of a hierarchy of classes implementing web applications
    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""
        dest = request.split()[4]
        return dest


    def process(self, parsedRequest):
        """Process the relevant elements of the request.
        Returns the HTTP code for the reply, and an HTML page.
        """
        newURL = parsedRequest+'/'+str(int(random.random() * 10000000))

        return ("200 OK", "<html><body><h1> Bienvenido al generador de URL's aleatorias.</h1>"+
                            "<p>"+
                            "<p>Tu siguiente URL(pincha con la rueda del raton): <a href='"+
                            newURL+"'>"+newURL+
                            "</a></p>"+
                            "</body></html>")

    def __init__(self, hostname, port):
        """Initialize the web application."""

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)
        try:
            while True:
                print('Waiting for connections')
                (recvSocket, address) = mySocket.accept()
                print('HTTP request received (going to parse and process):')
                request = recvSocket.recv(2048).decode('utf-8')
                print(request)
                parsedRequest = self.parse(request)
                (returnCode, htmlAnswer) = self.process(parsedRequest)
                print('Answering back...')
                recvSocket.send(bytes("HTTP/1.1 " + returnCode + " \r\n\r\n"
                                + htmlAnswer + "\r\n", 'utf-8'))
                recvSocket.close()
        except KeyboardInterrupt:
            print("Closing program")
            mySocket.close()

if __name__ == "__main__":
    testWebApp = webApp("localhost", 1234)
