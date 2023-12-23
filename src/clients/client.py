import socket
from typing import Tuple
import config


class Client:
    def __init__(self, host: str,
                 port: int,
                 ):
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__address = (host, port)

    def __str__(self):
        return f'{self.__address[0]}:{self.__address[1]}'

    def start_listening(self):
        self.socket.bind(self.__address)
        self.socket.listen()
        print(f'+ Server {self.__str__()} started.')

    def accept(self) -> Tuple[socket.socket, Tuple[str, int]]:
        return self.socket.accept()

    def close(self):
        self.socket.close()
