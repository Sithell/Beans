from greenstalk import Client, Job
from exception import ClientNotInitializedException
import strings
import tabulate


class Beans:
    def __init__(self):
        self.client: Client = None

    def help(self) -> None:
        print(strings.help)

    def connect(self, host: str = '127.0.0.1', port: int = 11300) -> bool:
        try:
            client: Client = Client((host, port))
            self.client = client
            return True

        except (ConnectionRefusedError, TimeoutError):
            return False

    def status(self) -> None:
        if self.client is None:
            raise ClientNotInitializedException()

        info: dict = self.client.stats()
        print(strings.status.format(info['version'], info['hostname']))
        result: list = []
        tubes: list = self.client.tubes()
        for tube in tubes:
            stats: dict = self.client.stats_tube(tube)
            result.append((tube, stats['current-jobs-ready']))

        print(tabulate.tabulate(result, headers=['Tube', 'Jobs ready']))

    def tube(self, tube: str = 'default') -> None:
        if self.client is None:
            raise ClientNotInitializedException()

        stats: dict = self.client.stats_tube(tube)
        self.client.use(tube)
        next_up: Job = self.client.peek_ready()
        print(strings.tube.format(
            tube,
            stats['current-jobs-ready'],
            stats['current-using'],
            stats['current-watching'],
            next_up.body
        ))

    def put(self, tube: str, body: str, priority: int = 65536, delay: int = 0) -> None:
        if self.client is None:
            raise ClientNotInitializedException()

        self.client.use(tube)
        print(self.client.put(body, priority, delay))

    def drain(self, tube: str) -> None:
        if self.client is None:
            raise ClientNotInitializedException()

        count: int = 0
        self.client.watch(tube)
        while True:
            if self.client.stats_tube(tube)['current-jobs-ready'] < 1:
                break

            job: Job = self.client.reserve()
            self.client.delete(job)
            count += 1

        print(f"Drained {count} jobs from {tube}")
