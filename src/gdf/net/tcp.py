#
# tcpip.py - TCP/IP реализация интернет соединения. Реализует класс для передачи данных через TCP/IP протокол.
#


# Импортируем:
if True:
    import time
    from threading import Thread
    from . import *


# Класс сервера TCP/IP:
class NetServerTCP:
    """ Пример функций-обработчиков:

    # Вызывается при присоединении клиента:
    def connect_handler(socket: NetSocket, address: tuple) -> None:
        pass

    # Вызывается каждый цикл сервера:
    def client_handler(socket: NetSocket, address: tuple) -> None:
        # Слушаем пинг клиента. Если его нет, то значит он отключился:
        if socket.recv_data() is None: socket.close()

        pass

    # Вызывается при отсоединении клиента:
    def disconnect_handler(socket: NetSocket, address: tuple) -> None:
        pass
    """

    # Инициализация:
    def __init__(self, connect_handler: any, client_handler: any, disconnect_handler: any) -> None:
        # Внутренние переменные класса:
        self.connect_handler    = connect_handler     # Вызывается при подключении клиента.
        self.client_handler     = client_handler      # Вызывается каждый цикл сервера.
        self.disconnect_handler = disconnect_handler  # Вызывается при отключении клиента.

        # Внутренние переменные:
        self.__netvars__ = {
            "clients":       [],      # Список клиентов.
            "connect-limit": int,     # Максимальное количество клиентов.
            "entry-key":     str,     # Ключ входа.
            "tps-limit":     float,   # Частота цикла обработки клиента (сколько раз в сек обработать).
            "timeout":       float,   # Время ожидания ответа между клиентом и сервером.
            "de-encoding":   "utf-8"  # Кодировка обменивания личными сообщениями между клиентом и сервером.
        }

        # Создаём сокет сервера (AF_INET это IPv4 | SOCK_STREAM это TCP):
        self.socket = NetSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

    # Обработчик клиентов в отдельном потоке:
    def __client_handler__(self, client: NetSocket, address: tuple) -> None:
        try:
            # Установка таймаута на ожидание ответа от клиента:
            client.set_time_out(self.__netvars__["timeout"])

            # Обрабатываем подключение клиента:
            self.connect_handler(client, address)

            while True:
                try:
                    # Смотрим данные, если есть пустое сообщение, то клиент отсоединился:
                    try:
                        # Отключаем блокировку:
                        client.set_blocking(False)

                        # Пробуем получить данные с флагом MSG_PEEK:
                        if not client.socket.recv(1, socket.MSG_PEEK): break
                    except BlockingIOError: pass
                    finally: client.set_blocking(True)

                    # Обрабатываем клиента:
                    self.client_handler(client, address)
                except (OSError, TimeoutError, socket.timeout):
                    break  # Выходим из бесконечного цикла обработки.

                # Делаем некоторую задержку между циклом, чтобы не взорвать провайдера:
                time.sleep(1/self.__netvars__["tps-limit"])

        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            raise NetConnectionLost(f"[009] Connection Lost (with {address[0]}:{address[1]})")

        finally:
            # Обрабатываем отключение клиента:
            self.disconnect_handler(client, address)

            # Удаляем этого клиента из списка:
            self.__netvars__["clients"].remove(client) if client in self.__netvars__["clients"] else None

            # Закрываем сокет клиента (соединение с клиентом) в любом случае:
            client.close()

    # Обработчик присоединений клиентов к серверу:
    def __connect_handler__(self) -> None:
        # Обрабатываем запросы на подключение:
        try:
            while True:
                try:
                    # Принимаем новое подключение клиента к серверу:
                    try: client, address = self.socket.accept()
                    except OSError as error: break
                    client = NetSocket(client)

                    # Добавляем клиента в список клиентов только если на сервере есть свободные места:
                    if self.get_connect_count() < self.__netvars__["connect-limit"]:
                        # Но перед добавлением в список, проверяем ключ клиента:
                        try:
                            # Даём клиенту timeout времени, чтобы тот предоставил ключ:
                            client.set_time_out(self.__netvars__["timeout"])

                            # Получаем ключ и преобразовываем его:
                            client_key = client.recv_data(1024, self.__netvars__["de-encoding"])
                            server_key = str(self.__netvars__["entry-key"])

                            # Проверяем ключ:
                            if client_key.strip() == server_key.strip():
                                # Если ключ правильный, то добавляем клиента в список:
                                self.__netvars__["clients"].append(client)

                                # Сообщаем клиенту, что тот прошёл:
                                client.send_data("key-success", self.__netvars__["de-encoding"])

                                # Создаём новый демонический поток для обработки клиента:
                                Thread(target=self.__client_handler__, args=(client, address), daemon=True).start()
                            else:
                                # Если ключ клиента не подходит, то сообщаем ему об этом, и отключаем от сервера:
                                client.send_data("key-wrong", self.__netvars__["de-encoding"])
                                client.close()
                        except socket.timeout:
                            # Если клиент не успел предоставить ключ, то сообщаем ему об этом и отключаем его:
                            client.send_data("key-timeout-error", self.__netvars__["de-encoding"])
                            client.close()
                    else:
                        # Если сервер переполнен:
                        client.send_data("server-overflow", self.__netvars__["de-encoding"])
                        client.close()
                except socket.timeout:
                    client.close()
                    raise NetConnectionTimeOut("[002] Connection Timeout. The client is not responding.")
                except OSError as error:
                    client.close()
                    if error.errno == 10038:
                        raise NetException(
                            "[005] Server Error: An attempt was made to perform "
                            "an operation on an object that is not a socket")
                    else: raise NetException(f"[000] Unknown error (in NetServerTCP.__connect_handler__()): {error}")
        except Exception as error:
            raise NetException(f"[005] Server Error: {error}")
        finally: self.socket.close()

    # Создать сервер:
    def create(self,
               host:          str,
               port:          int,
               key:           str   = None,
               tps:           float = 60.0,
               connect_limit: int   = 4,
               listen_limit:  int   = 4,
               timeout:       float = 10.0
               ) -> "NetServerTCP":
        # Подключаем сокет сервера к IP и порту:
        try: self.socket.bind(host, port)
        except OSError as error:
            self.socket.close()
            if   error.errno == 10049: raise NetException("[007] Address server is being created is invalid.")
            elif error.errno == 10048: raise NetException("[006] The selected Port is already occupied.")
            else:                      raise NetException(f"[000] Unknown error: {error}")

        # Устанавливаем максимальное количество клиентов:
        self.set_connect_limit(max(int(connect_limit), 0))

        # Устанавливаем ограничение количества удерживаемых клиентов для подключения:
        self.set_listen_limit(max(int(listen_limit), 0))

        # Устанавливаем максимальное время ожидания ответа от клиента:
        self.set_timeout(timeout)

        # Ключ входа:
        self.__netvars__["entry-key"] = key.strip() if key is not None else None

        # TPS сервера:
        self.__netvars__["tps-limit"] = tps

        # Создаём новый демонический поток для обработки входящих подключений:
        Thread(target=self.__connect_handler__, args=(), daemon=True).start()

        return self

    # Установить максимальное количество поключаемых клиентов:
    def set_connect_limit(self, connect_limit: int) -> "NetServerTCP":
        self.__netvars__["connect-limit"] = connect_limit
        return self

    # Установить максимальное количество поключаемых клиентов:
    def set_listen_limit(self, listen_limit: int) -> "NetServerTCP":
        self.socket.listen(listen_limit)
        return self

    # Установить таймаута ожидания ответа:
    def set_timeout(self, timeout: float) -> "NetServerTCP":
        self.__netvars__["timeout"] = timeout
        return self

    # Получить количество соединений (клиентов):
    def get_connect_count(self) -> int:
        return len(self.__netvars__["clients"])

    # Получить ip сервера:
    def get_host(self) -> str:
        return self.socket.get_host()

    # Получить порт сервера:
    def get_port(self) -> int:
        return self.socket.get_port()

    # Отключить всех клиентов:
    def disconnect_all(self) -> "NetServerTCP":
        # Отключаем всех клиентов и очищаем список клиентов:
        for c in list(self.__netvars__["clients"]): c.close()
        self.__netvars__["clients"].clear()

        return self

    # Отключить сервер (сеть):
    def destroy(self) -> None:
        # Отключаем всех клиентов и останавливаем сервер:
        self.disconnect_all()
        self.socket.close()


# Класс клиента TCP/IP:
class NetClientTCP:
    """ Пример функций-обработчиков:

    # Вызывается при присоединении к серверу:
    def connect_handler(socket: NetSocket, address: tuple) -> None:
        pass

    # Вызывается каждый цикл клиента:
    def server_handler(socket: NetSocket, address: tuple) -> None:
        # Слушаем пинг сервера. Если его нет, то значит сервер отключился:
        if socket.recv_data() is None: socket.close()

        pass

    # Вызывается при потери связи с сервером:
    def disconnect_handler(socket: NetSocket, address: tuple) -> None:
        pass
    """

    # Инициализация:
    def __init__(self, connect_handler: any, server_handler: any, disconnect_handler: any) -> None:
        # Внутренние переменные:
        self.connect_handler    = connect_handler     # Вызывается при подключении к серверу.
        self.server_handler     = server_handler      # Вызывается каждый 1/TPS раз в отдельном потоке.
        self.disconnect_handler = disconnect_handler  # Вызывается при отключении от сервера.

        self.__netvars__ = {
            "tps-limit":   float,   # Частота цикла обработки сервера (сколько раз в сек обработать).
            "timeout":     float,   # Время ожидания ответа между клиентом и сервером.
            "de-encoding": "utf-8"  # Кодировка обменивания личными сообщениями между клиентом и сервером.
        }

        # Создаём сокет клиента (AF_INET это IPv4 | SOCK_STREAM это TCP):
        self.socket = NetSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

    # Обработчик сервера в отдельном потоке:
    def __server_handler__(self, server: NetSocket, address: tuple) -> None:
        try:
            # Установка таймаута на ожидание ответа от сервера:
            server.set_time_out(self.__netvars__["timeout"])

            # Обрабатываем подключение:
            self.connect_handler(server, address)

            while True:
                try:
                    # Смотрим данные, если есть пустое сообщение, то сервер отсоединился:
                    try:
                        # Отключаем блокировку:
                        server.set_blocking(False)

                        # Пробуем получить данные с флагом MSG_PEEK:
                        if not server.socket.recv(1, socket.MSG_PEEK): break
                    except BlockingIOError: pass
                    finally: server.set_blocking(True)

                    # Обрабатываем сервер:
                    self.server_handler(server, address)
                except (OSError, TimeoutError, socket.timeout):
                    break

                # Делаем некоторую задержку между циклом, чтобы не взорвать провайдера:
                time.sleep(1/self.__netvars__["tps-limit"])

        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            raise NetConnectionLost("[009] Connection Lost.")

        finally:
            self.disconnect()

    # Подключиться к серверу:
    def connect(self,
                host:    str,
                port:    int,
                key:     str   = None,
                tps:     float = 60.0,
                timeout: float = 10.0
                ) -> "NetClientTCP":
        # Устанавливаем тайм-аут на ожидание подтверждения подключения к серверу:
        self.socket.set_time_out(timeout+0.1)  # +0.1 секунда, на всякий случай.

        try:
            # Подключаемся к серверу:
            self.socket.connect(host, port)
            serv_addr = self.socket.get_peer_name()

            # Сразу отправляем ключ входа:
            self.socket.send_data(key,  self.__netvars__["de-encoding"])

            # Получаем ответ от сервера:
            data = self.socket.recv_data(1024,  self.__netvars__["de-encoding"])

            # Если ключ не правильный:
            if data == "key-wrong":
                self.socket.close()
                raise NetClientKeyWrong("[010] Server disconnected you due to an incorrect password.")

            # Иначе если время за которое мы должны были отправить ключ, вышло:
            elif data == "key-timeout-error":
                self.socket.close()
                raise NetTimeOut("[011] Server disconnected you because it didn't wait for the password.")

            # Иначе если сервер переполнен:
            elif data == "server-overflow":
                self.socket.close()
                raise NetServerOverflow("[012] Server disconnected you because server is full.")

            # Иначе если ключ правильный:
            elif data == "key-success":
                # Устанавливаем максимальное время ожидания ответа от сервера:
                self.set_timeout(timeout)

                # TPS клиента:
                self.__netvars__["tps-limit"] = tps

                # Создаём новый демонический поток для обработки сервера:
                Thread(target=self.__server_handler__, args=(self.socket, serv_addr), daemon=True).start()
            else:
                raise NetException(f"[013] Connection was not established for an unknown reason: {data}")

        except socket.gaierror:
            self.socket.close()
            raise NetException("[004] The specified hostname does not exist or cannot be resolved.")

        except socket.timeout:
            self.socket.close()
            raise NetConnectionTimeOut("[002] Connection Timeout. Server too long to process the connection.")

        except ConnectionRefusedError:
            self.socket.close()
            raise NetConnectionRefused("[003] Connection refused.")

        except (ConnectionAbortedError, ConnectionResetError):
            self.socket.close()
            raise NetConnectionLost("[009] Connection Lost.")

        except OSError as error:
            self.socket.close()
            if error.errno == 10049:
                raise NetException("[001] Invalid server address.")
            else: raise NetException(f"[000] Unknown error: {error}")

        return self

    # Установить таймаута ожидания ответа:
    def set_timeout(self, timeout: float) -> "NetClientTCP":
        self.__netvars__["timeout"] = timeout
        return self

    # Получить ip клиента:
    def get_host(self) -> str:
        return self.socket.get_host()

    # Получить порт клиента:
    def get_port(self) -> int:
        return self.socket.get_port()

    # Отключаемся от сервера:
    def disconnect(self) -> "NetClientTCP":
        # Обрабатываем отключение от сервера:
        self.disconnect_handler(self.socket, self.socket.get_peer_name())

        # Закрываем сокет клиента (соединение с клиентом) в любом случае:
        self.socket.close()

        return self

    # Отключить клиента от сервера:
    def destroy(self) -> None:
        self.disconnect()
