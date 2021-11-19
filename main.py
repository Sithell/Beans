from exception import InvalidArgumentException
import greenstalk
import strings
import sys


# noinspection PyShadowingNames
def process_input(args):
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


def command_help():
    print(strings.help)


# noinspection PyShadowingNames
def command_connect(arguments):
    host, port = arguments
    try:
        client = greenstalk.Client((host, port))
        client.close()
        with open('config', 'w') as f:
            print(host, port, sep='\n', file=f)

        print("Connected successfully")

    except ConnectionRefusedError:
        print(f"Invalid credentials: {host}:{port}")


if __name__ == "__main__":
    command, arguments, options = process_input(sys.argv)
    if command == 'help':
        command_help()
    elif command == 'connect':
        command_connect(arguments)
