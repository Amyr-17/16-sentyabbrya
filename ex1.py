class Data:
    """Класс для описания пакета информации"""
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip


class Server:
    """Класс для описания работы серверов в сети"""
    _ip_counter = 0  # Счетчик для автоматической выдачи IP

    def __init__(self):
        Server._ip_counter += 1
        self.ip = Server._ip_counter
        self.buffer = []

    def send_data(self, data):
        """Отправка информационного пакета роутеру"""
        if hasattr(self, '_router') and self._router is not None:
            self._router.buffer.append(data)

    def get_data(self):
        """Возврат списка принятых пакетов и очистка буфера"""
        received = self.buffer[:]
        self.buffer.clear()
        return received

    def get_ip(self):
        """Возврат своего IP-адреса"""
        return self.ip


class Router:
    """Класс для описания работы роутера в сети"""
    def __init__(self):
        self.buffer = []
        self.servers = {}

    def link(self, server):
        """Присоединение сервера к роутеру"""
        self.servers[server.get_ip()] = server
        server._router = self  # Даем серверу ссылку на роутер

    def unlink(self, server):
        """Отсоединение сервера от роутера"""
        if server.get_ip() in self.servers:
            del self.servers[server.get_ip()]
        if hasattr(server, '_router'):
            server._router = None

    def send_data(self):
        """Отправка всех пакетов из буфера соответствующим серверам"""
        for packet in self.buffer:
            target_ip = packet.ip
            if target_ip in self.servers:
                self.servers[target_ip].buffer.append(packet)
        self.buffer.clear()
