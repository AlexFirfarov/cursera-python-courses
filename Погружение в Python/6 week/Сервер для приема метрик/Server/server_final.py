import asyncio


class ServerError(Exception):
    pass


class Data:
    data = dict()


async def server_func(reader, writer):
    while True:
        request = await reader.read(1024)
        if not request:
            break
        message = request.decode()

        try:
            if not message.endswith('\n'):
                raise ServerError
            message = message[0:-1].split(sep=' ')

            if message[0] not in ('put', 'get'):
                raise ServerError
            if message[0] == 'put':
                if len(message) != 4:
                    raise ServerError
                key, value, timestamp = message[1], float(message[2]), int(message[3])

                if key not in Data.data.keys():
                    Data.data[key] = []
                key_data = Data.data[key]
                replaced = False
                for i in range(0, len(key_data)):
                    if timestamp in key_data[i]:
                        key_data[i] = (value, timestamp)
                        replaced = True
                        break
                if not replaced:
                    Data.data[key].append((value, timestamp))
                writer.write(b'ok\n\n')

            if message[0] == 'get':
                if len(message) != 2:
                    raise ServerError
                key = message[1]

                if key not in Data.data.keys() and key != '*':
                    writer.write(b'ok\n\n')
                else:
                    keys = Data.data.keys() if key == '*' else [key]
                    response = 'ok\n'
                    for key_dict in keys:
                        for value, timestamp in Data.data[key_dict]:
                            response += key_dict + ' ' + str(value) + ' ' + str(timestamp) + '\n'
                    response += '\n'
                    writer.write(response.encode())

        except Exception:
            error_response = 'error\nwrong command\n\n'
            writer.write(error_response.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(server_func, host, port, loop=loop)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server("127.0.0.1", 8888)
