from exception import (
    BeansException,
    InvalidArgumentException,
    InvalidCredentialsException,
    MissingArgumentException,
    NotEnoughArgumentsException,
)
from beans import Beans
import sys
from configparser import ConfigParser


class Console:
    def __init__(self, beans: Beans, config: ConfigParser):
        self.beans: Beans = beans
        self.config: ConfigParser = config
        pass

    def command_help(self, *args, **kwargs) -> None:
        self.beans.help()

    def command_connect(self, *args, **kwargs) -> None:
        host: str = None
        port: int = None
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
            raise InvalidCredentialsException(host, port)

    def command_status(self, *args, **kwargs) -> None:
        if self.client_connected():
            self.beans.status()

    def command_tube(self, *args, **kwargs) -> None:
        if len(args) < 1:
            raise MissingArgumentException('tube')

        tube: str = args[0]

        if self.client_connected():
            self.beans.tube(tube)

    def command_drain(self, *args, **kwargs) -> None:
        if len(args) < 1:
            raise MissingArgumentException('tube')

        tube: str = args[0]

        if self.client_connected():
            self.beans.drain(tube)

    def command_put(self, *args, **kwargs) -> None:
        if len(args) < 2:
            raise NotEnoughArgumentsException(2, len(args))

        tube: str = args[0]
        body: str = args[1]

        if self.client_connected():
            self.beans.put(tube, body)

    def client_connected(self) -> bool:
        host: str = self.config.get('beanstalkd', 'host')
        port: int = self.config.getint('beanstalkd', 'port')
        if not self.beans.connect(host, port):
            raise InvalidCredentialsException(host, port)

        return True

    # noinspection PyShadowingNames
    def process_input(self, args: list) -> list:
        command: str = None
        options: dict = {}
        arguments: list = []
        if len(args) > 1:
            for i in range(1, len(args)):
                if args[i][0] == '-':
                    if args[i].count('=') > 1:
                        raise InvalidArgumentException(args[i])

                    if args[i].count('=') == 1:
                        option: str
                        value: str
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
                command: str = arguments[0]
                arguments.pop(0)

        return [command, arguments, options]


if __name__ == "__main__":
    config: ConfigParser = ConfigParser()
    config.read('config.ini')

    beans: Beans = Beans()
    console: Console = Console(beans, config)

    command: str
    arguments: list
    options: dict
    command, arguments, options = console.process_input(sys.argv)

    bindings: dict = {
        'help': console.command_help,
        'connect': console.command_connect,
        'status': console.command_status,
        'tube': console.command_tube,
        'drain': console.command_drain,
        'put': console.command_put,
    }

    if command in bindings:
        try:
            bindings[command](*arguments, **options)

        except BeansException as e:
            print("Error:", e.get_message())

    else:
        print("Unknown command")
