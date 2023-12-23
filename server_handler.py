import config
from src.clients.server_client import ServerClient
from src.services_signatures import ServicesSignatures
from src.rpc_server import RpcServer


def server_handler():
    client = ServerClient(host=config.HOST, port=config.PORT)
    cache = dict()
    services = ServicesSignatures(cache=cache)
    RpcServer(client=client, services=services).run()


if __name__ == "__main__":
    server_handler()
