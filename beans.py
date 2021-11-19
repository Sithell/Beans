import greenstalk
import strings


class Beans:
    def __init__(self):
        self.client = None

    def help(self):
        print(strings.help)

    def connect(self, host='127.0.0.1', port=11300) -> bool:
        try:
            client = greenstalk.Client((host, port))
            self.client = client
            return True

        except ConnectionRefusedError:
            return False
