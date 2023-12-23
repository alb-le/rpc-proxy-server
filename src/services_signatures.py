import socket
from typing import Any, Tuple, List, Dict, Optional

import config
from src.clients.server_client import ServerClient


class ServicesSignatures:
    def __init__(self, cache: dict):
        self.__num_functions = {
            'sum': self.__my_sum,
            'min': self.__my_min,
        }
        self.__str_functions = {
            'split': self.__my_split,
        }
        self.__cached_responses = cache

    def __help(self, *arg, **kwargs):
        return f'List of functions using strings as arguments:\n{list(self.__str_functions.keys())}\n' \
               f'List of functions using numbers as arguments:\n{list(self.__num_functions.keys())}'

    def __invalid_function_call(self):
        return 'There is no available function with that signature. ' + self.__help()

    def __my_sum(self, left: int, right: int) -> int:
        res = self.__call_num_service('sum', left, right)
        return res

    def __my_min(self, left: Any, right: Any) -> bool:
        res = self.__call_num_service('min', left, right)
        return res

    def __my_split(self, s: str) -> List[str]:
        res = self.__call_str_service('split', s)
        return res

    def run_fn(self, request: List):
        function_type, function_name, args, kwargs = self.__get_call_signature(request)

        if cached_res := self.__get_cached_response(function_name, args, kwargs):
            return cached_res

        match function_type:
            case 'help':
                return self.__help()

            case 'error':
                return self.__invalid_function_call()

            case 'string':
                res = self.__str_functions[function_name](*args, **kwargs)
                self.__save_response_on_cache(function_name, args, kwargs, res)
                return res

            case 'numeral':
                res = self.__num_functions[function_name](*args, **kwargs)
                self.__save_response_on_cache(function_name, args, kwargs, res)
                return res

    def __get_call_signature(self, request: list) -> Tuple[str, str, Optional[List], Optional[Dict]]:
        function_name = request[0].lower()

        if function_name in 'help':
            function_type = 'help'

        elif function_name in self.__num_functions.keys():
            function_type = 'numeral'

        elif function_name in self.__str_functions.keys():
            function_type = 'string'

        else:
            function_type = 'error'

        args = request[1]
        kwargs = request[2]
        return function_type, function_name, args, kwargs

    def __get_cached_response(self, function_name, args, kwargs):
        signature = self.__get_call_signature_as_str(function_name, args, kwargs)
        return self.__cached_responses.get(signature, None)

    @staticmethod
    def __get_call_signature_as_str(function_name, args, kwargs) -> str:
        return f"{function_name}{args}{kwargs}"

    def __save_response_on_cache(self, function_name, args, kwargs, res):
        self.__cached_responses[self.__get_call_signature_as_str(function_name, args, kwargs)] = res

    @staticmethod
    def __call_num_service(fn_name, *args, **kwargs):
        service_client = ServerClient()

        try:
            service_client.handshake(port=config.NUM_SERVICE_PORT)
            res = service_client.call_fn(fn_name, args, kwargs)
            service_client.close()

        except Exception as ex:
            res = str(ex)
            print(f'[ERROR] Error calling fn {fn_name}: {res}')
            service_client.close()
            raise ex

        return res

    @staticmethod
    def __call_str_service(self, fn_name, *args, **kwargs):
        service_client = ServerClient()

        try:
            service_client.handshake(port=config.STR_SERVICE_PORT)
            res = service_client.call_fn(fn_name, args, kwargs)
            service_client.close()

        except Exception as ex:
            res = str(ex)
            print(f'[ERROR] Error calling fn {fn_name}: {res}')
            service_client.close()
            raise ex

        return res
