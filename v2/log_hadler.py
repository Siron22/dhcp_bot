import re


class DhcpLogHandler:

    def __init__(self, path='/var/log/syslog'):
        self.path = path
        self.devices = []

    def _get_ack_log(self):
        try:
            with open(self.path, 'r') as f:
                log = f.read()
                dhcpack = re.findall(r'.*DHCPACK.*', log)
                return dhcpack
        except FileNotFoundError:
            print(f"File {self.path} not found.")
            return ""
    @staticmethod
    def _extract_device(line):
        device = dict()
        ip_address_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
        mac_address_match = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', line)
        device["ip"] = ip_address_match.group() if ip_address_match else None
        device["mac"] = mac_address_match.group() if mac_address_match else None
        return device

    def approved_addresses(self):
        log = self._get_ack_log()
        for line in log:
            new_device = self._extract_device(line)
            if new_device["mac"] and not any(added_device.get("mac") == new_device["mac"] for added_device in self.devices):
                self.devices.append(new_device)
        return self.devices

    def monitor_dhcp_log(self):
        prev_requests = 0
        while True:
            with open(self.path, 'r') as file:
                log_content = file.read()

            current_connections = get_all_connections(log_content)

            if current_connections != prev_requests:
                print(
                    f"Изменение! Текущее количество подключенных устройств (включая отключенные): {current_connections}")
                prev_requests = current_connections

            time.sleep(5)


# Пример использования
log_handler = DhcpLogHandler()
connected_devices = log_handler.approved_addresses()

if connected_devices:
    print(f"{len(connected_devices)} addresses approved for devices:")
    for device in connected_devices:
        print(f"mac: {device['mac']}, ip: {device['ip']}")
else:
    print("Нет подключенных устройств.")
