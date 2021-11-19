from exception import InvalidArgumentException
from beans import Beans
import sys
import configparser


class Console:
    def __init__(self, beans, config):
        self.beans = beans
        self.config: configparser.ConfigParser = config
        pass

    def command_help(self, *args, **kwargs):
        self.beans.help()

    def command_connect(self, *args, **kwargs):
        host, port = None, None
        if 'host' in kwargs:
            host = kwargs['host']

        elif len(args) > 0:
            host = args[0]

        if 'port' in kwargs:
            port = kwargs['port']

        elif len(args) > 1:
            port = args[1]

        if self.beans.connect(host, port):
            if not self.config.has_section('beanstalkd'):
                self.config.add_section('beanstalkd')

            self.config.set('beanstalkd', 'host', host)
            self.config.set('beanstalkd', 'port', port)
            with open('config.ini', 'w') as f:
                self.config.write(f)

        else:
            print(f"Invalid credentials: {host}:{port}")

    def command_status(self, *args, **kwargs):
        if self.client_connected():
            self.beans.status()

    def command_tube(self, *args, **kwargs):
        if len(args) < 1:
            raise Exception("Missing argument: tube")

        tube = args[0]

        if self.client_connected():
            self.beans.tube(tube)

    def command_drain(self, *args, **kwargs):
        if len(args) < 1:
            raise Exception("Missing argument: tube")

        tube = args[0]

        if self.client_connected():
            self.beans.drain(tube)

    def command_put(self, *args, **kwargs):
        if len(args) < 2:
            raise Exception("Not enough arguments")

        tube = args[0]
        body = args[1]

        if self.client_connected():
            self.beans.put(tube, body)

    def client_connected(self) -> bool:
        host, port = self.config.get('beanstalkd', 'host'), self.config.getint('beanstalkd', 'port')
        if not self.beans.connect(host, port):
            print(f"Invalid credentials: {host}:{port}")

    # noinspection PyShadowingNames
    def process_input(self, args):
        command = None
        options = {}
        arguments = []
        if len(args) > 1:
            for i in range(1, len(args)):
                if args[i][0] == '-':
                    if args[i].count('=') > 1:
                        raise InvalidArgumentException(args[i])

                    if args[i].count('=') == 1:
                        option, value = args[i].split('=')
                        if option[1] == '-':
                            option = option[2:]

                        else:
                            option = option[1:]

                        options[option] = value

                    if args[i].count('=') == 0:
                        if args[i][1] == '-':
                            option = args[i][2:]

                        else:
                            option = args[i][1:]

                        options[option] = True

                else:
                    arguments.append(args[i])

            if len(arguments) > 0:
                command = arguments[0]
                arguments.pop(0)

        return [command, arguments, options]


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    beans = Beans()
    console = Console(beans, config)

    command, arguments, options = console.process_input(sys.argv)

    bindings = {
        'help': console.command_help,
        'connect': console.command_connect,
        'status': console.command_status,
        'tube': console.command_tube,
        'drain': console.command_drain,
        'put': console.command_put,
    }

    if command in bindings:
        bindings[command](*arguments, **options)

    else:
        print("Unknown command")
