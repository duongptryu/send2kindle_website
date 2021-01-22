
import re
import threading
import socket


class portscan():
    def __init__(self, subdomains, ports):
        self.subdomains = subdomains
        self.ports = ports
        self.lock = None

    def port_scan(self, host, ports, sublistPort):
        self.lock.acquire()
        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                result = s.connect_ex((host, int(port)))
                if result == 0:
                    sublistPort.append(host)
                s.close()
            except Exception:
                pass
        self.lock.release()

    async def run(self):
        sublistPort = []
        threads = list()

        self.lock = threading.BoundedSemaphore(value=20)
        for subdomain in self.subdomains:
            t = threading.Thread(target=self.port_scan,
                                 args=(subdomain, self.ports, sublistPort))
            threads.append(t)
            t.start()

        for thread in threads:
            thread.join(0.5)

        # time.sleep(180)
        return sublistPort