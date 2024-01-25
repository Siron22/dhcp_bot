import re


class DhcpLogHandler:

    def __init__(self, path='/app/log/syslog'):
        self.path = path
        self.devices = list()
        self.new = list()
        self.ack_log = self._get_ack_log()
        self._add_new_device(self.ack_log)

    def _get_ack_log(self):
        try:
            with open(self.path, 'r') as f:
                dhcpack = re.findall(r'.*DHCPACK.*', f.read())
                log = [self._extract_client_info(line) for line in dhcpack]
                return log
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.path} not found.")

    @staticmethod
    def _extract_client_info(line):
        client = dict()
        ip_address_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
        mac_address_match = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', line)
        date_time_match = re.search(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s\d{2}:\d{2}:\d{2}\b', line)
        client["date_time"] = date_time_match.group() if date_time_match else None
        client["ip"] = ip_address_match.group() if ip_address_match else None
        client["mac"] = mac_address_match.group() if mac_address_match else None
        return client

    def _add_new_device(self, log):
        new_devices = []
        for new_device in log:
            if new_device["mac"] and new_device["mac"] not in [device["mac"] for device in self.devices]:
                self.devices.append(new_device)
                new_devices.append(new_device)
        return new_devices

    @property
    def get_approved_devices(self):
        return self.devices

    @property
    def get_ack_requests(self):
        return self.ack_log

    @property
    def get_new(self):
        return self.new

    def clear_new(self):
        self.new.clear()

    def monitor_dhcp_log(self):
        current_log = self._get_ack_log()
        if len(current_log) > len(self.ack_log):
            delta = len(self.ack_log) - len(current_log)
            new = self._add_new_device(current_log[delta:])
            if new:
                self.new.append(new)
            self.ack_log = current_log
            return current_log[delta:]


"""dhcp = DhcpLogHandler()

print(dhcp.get_ack_requests)
print(dhcp.get_approved_devices)

while True:
    print(dhcp.monitor_dhcp_log())
    time.sleep(3)"""
