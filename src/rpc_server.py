import socket
import traceback
from threading import Thread
from typing import Tuple

from src.clients.server_client import ServerClient
from src.my_exception import DisconnectedException
from src.services_signatures import ServicesSignatures


class RpcServer:
    def __init__(self, client: ServerClient, services: ServicesSignatures):
        self.client: ServerClient = client
        self.services = services

    def __multithread_handler(self, worker_socket: socket.socket, address: Tuple[str, int]):
        try:
            client_address = f'{address[0]}:{address[1]}'
            print(f'Managing requests from {client_address}.')
            while True:

                try:
                    request = self.client.receive_to_worker(worker_socket)
                    print(f'[INFO] {client_address} -> Request: {request}.')
                    response = self.services.run_fn(request)
                    print(f'[INFO] Response: {response}')
                    self.client.send(socket_=worker_socket, payload=response)

                except DisconnectedException:
                    print(f'[INFO] Client {client_address} disconnected.')
                    break

                except Exception as ex:
                    error_res = f'{str(ex)}\n\n{traceback.print_exc()}'
                    print(f'[ERROR] {error_res}')
                    self.client.send(socket_=worker_socket, payload=error_res)
                    raise ex

        finally:
            self.client.close_worker_socket(worker_socket)

    def run(self) -> None:
        self.client.start_listening()
        while True:
            try:
                client, address = self.client.accept()
                Thread(target=self.__multithread_handler, args=[client, address]).start()

            except KeyboardInterrupt:
                self.client.close()
                print(f'- Server {self.client} interrupted.')
                break

            except Exception as ex:
                self.client.close()
                raise ex
