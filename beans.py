import greenstalk
import strings


class Beans:
    def help(self):
        print(strings.help)

    def connect(self, host='127.0.0.1', port=11300):
        try:
            client = greenstalk.Client((host, port))
            client.close()
            with open('config', 'w') as f:
                print(host, port, sep='\n', file=f)

            print("Connected successfully")

        except ConnectionRefusedError:
            print(f"Invalid credentials: {host}:{port}")
