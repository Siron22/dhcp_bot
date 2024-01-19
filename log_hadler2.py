import re


class DhcpLogHandler:

    def __init__(self, path='/var/log/syslog'):
        self.path = path
        self.log = self._get_log()
        self.devices = []

    def _get_log(self):
        try:
            with open(self.path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Файл {self.path} не найден.")
            return ""

    def _extract_device(self, line):
        device = dict()
        ip_address_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
        mac_address_match = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', line)
        device["number"] = 1
        device["ip"] = ip_address_match.group() if ip_address_match else None
        device["mac"] = mac_address_match.group() if mac_address_match else None
        return device

    def connected_devices(self):
        matches = re.findall(r'.*DHCPACK.*', self.log)
        for line in matches:
            new_device = self._extract_device(line)
            if new_device["mac"] and not any(added_device.get("mac") == new_device["mac"] for added_device in self.devices):
                self.devices.append(new_device)
        return self.devices

# Пример использования
"""log_handler = DhcpLogHandler()
connected_devices = log_handler.connected_devices()

if connected_devices:
    print(f"{len(connected_devices)} устройств подключено:")
    for device in connected_devices:
        print(f"mac: {device['mac']}, ip: {device['ip']}")
else:
    print("Нет подключенных устройств.")"""
