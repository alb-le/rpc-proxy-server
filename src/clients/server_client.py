import json
import socket

import config
from src.clients.client import Client
from src.my_exception import DisconnectedException


class ServerClient(Client):
    def __init__(self, host: str = '127.0.0.1', port: int = 0):
        super().__init__(host, port)

    @staticmethod
    def get_address(socket_: socket.socket) -> str:
        socket_address = socket_.getsockname()
        return f'{socket_address[0]}:{socket_address[1]}'

    @staticmethod
    def send(socket_: socket.socket, payload: str):
        socket_.sendall(json.dumps(payload).encode())

    @staticmethod
    def receive_to_worker(worker_socket: socket.socket) -> list:
        res = worker_socket.recv(config.MSG_SIZE).decode()
        if not res:
            raise DisconnectedException
        res_obj = json.loads(res)
        print(f'[DEBUG] Response: {res_obj}')
        return res_obj

    @staticmethod
    def close_worker_socket(worker_socket: socket.socket):
        worker_socket.close()

    def handshake(self, port: int, host: str = 'localhost'):
        self.socket.connect((host, port))

    def call_fn(self, fn_name: str, args: tuple, kwargs: dict):
        args_s = ', '.join(args)
        if kwargs:
            kwargs_s = ', '.join([f'{k}= {v}' for k, v in kwargs.items()])
            if args:
                s = args_s + ', ' + kwargs_s
            else:
                s = kwargs_s
        else:
            s = args_s

        signature = f'{fn_name}({s})'

        self.socket.sendall(json.dumps(signature).encode())
        res = self.socket.recv(config.MSG_SIZE).decode()
        return json.loads(res)
