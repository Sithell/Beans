import greenstalk
import strings


class Beans:
    def __init__(self):
        self.client: greenstalk.Client = None

    def help(self):
        print(strings.help)

    def connect(self, host='127.0.0.1', port=11300) -> bool:
        try:
            client = greenstalk.Client((host, port))
            self.client = client
            return True

        except (ConnectionRefusedError, TimeoutError):
            return False

    def status(self):
        if self.client is None:
            raise Exception("Client not initialized")

        info = self.client.stats()
        print(strings.status.format(info['version'], info['hostname']))
        tubes = self.client.tubes()
        for tube in tubes:
            stats = self.client.stats_tube(tube)
            print(f"{tube}: {stats['current-jobs-ready']}")

    def tube(self, tube='default'):
        if self.client is None:
            raise Exception("Client not initialized")

        stats = self.client.stats_tube(tube)
        self.client.use(tube)
        next_up = self.client.peek_ready()
        print(strings.tube.format(
            tube,
            stats['current-jobs-ready'],
            stats['current-using'],
            stats['current-watching'],
            next_up.body
        ))

    def put(self, tube, body, priority=65536, delay=0):
        if self.client is None:
            raise Exception("Client not initialized")

        self.client.use(tube)
        print(self.client.put(body, priority, delay))

    def drain(self, tube):
        if self.client is None:
            raise Exception("Client not initialized")

        count = 0
        self.client.watch(tube)
        while True:
            if self.client.stats_tube(tube)['current-jobs-ready'] < 1:
                break

            job = self.client.reserve()
            self.client.delete(job)
            count += 1

        print(f"Drained {count} jobs from {tube}")
