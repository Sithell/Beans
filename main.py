from exception import InvalidArgumentException
from beans import Beans
import sys


class Console:
    def __init__(self, beans):
        self.beans = beans
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
            with open('config', 'w') as f:
                print(host, port, sep='\n', file=f)

        else:
            print(f"Invalid credentials: {host}:{port}")

    def command_status(self, *args, **kwargs):
        f = open('config', 'r')
        config = f.readlines()
        host, port = config[0].strip(), config[1].strip()
        if not self.beans.connect(host, port):
            print(f"Invalid credentials: {host}:{port}")
        else:
            self.beans.status()

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
    beans = Beans()
    console = Console(beans)

    command, arguments, options = console.process_input(sys.argv)

    bindings = {
        'help': console.command_help,
        'connect': console.command_connect,
        'status': console.command_status
    }

    if command in bindings:
        bindings[command](*arguments, **options)

    else:
        print("Unknown command")
