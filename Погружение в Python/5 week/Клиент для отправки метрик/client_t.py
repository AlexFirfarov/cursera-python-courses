import socket
import time


class ClientError(Exception):

    def __init__(self):
        pass


class Client:

    def __init__(self, host, port, timeout=None):
        self.sock = socket.create_connection((host, port), timeout)

    def put(self, metric, value, timestamp=None):
        timestamp = timestamp or int(time.time())
        request = "put {0} {1} {2}\n".format(metric, value, timestamp)
        self.sock.sendall(request.encode("utf8"))
        message = self.sock.recv(1024).decode("utf8")

        if message != "ok\n\n":
            raise ClientError

    def get(self, metric):
        request = "get {0}\n".format(metric)
        print(request)
        self.sock.sendall(request.encode("utf8"))
        message = self.sock.recv(1024).decode("utf8")
        split_message = message.splitlines()

        if len(split_message) == 0 or split_message.pop() != '':
            raise ClientError
        if split_message[0] != "ok":
            raise ClientError
        if len(split_message) == 1:
            return {}

        dictionary = dict()
        for str in split_message:
            if str == "ok":
                continue
            dict_elem = str.split(sep=' ')
            if len(dict_elem) != 3:
                raise ClientError

            key = dict_elem[0]
            value = dict_elem[1]
            timestamp = dict_elem[2]

            dictionary.setdefault(key, [])
            try:
                dictionary[key].append((int(timestamp), float(value)))
            except Exception:
                raise ClientError

            for key in dictionary.keys():
                dictionary[key].sort(key=lambda x: x[0])

        return dictionary
