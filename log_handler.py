import re
from datetime import datetime


class DhcpLogHandler:

    def __init__(self, path):
        self.path = path
        self.log = self._get_log()
        self.devices = []

    def _get_log(self):
        try:
            with open(self.path, 'r') as f:
                result = f.read()
            return result
        except FileNotFoundError:
            print(f"Файл {self.path} не найден.")
            return ""

    def _extract_device(self, line):
        device = dict()
        ip_address_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
        mac_address_match = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', line)
        device["number"] = 1
        device["ip"] = ip_address_match.group()
        device["mac"] = mac_address_match.group()
        return device

    def connected_devices(self):
        matches = re.findall(r'.*DHCPACK.*', self.log)
        for line in matches:
            new_device = self._extract_device(line)
            if not any(added_device.get("mac") == new_device["mac"] for added_device in self.devices):
                self.devices.append(new_device)
        quantity = len(self.devices)
        message = (f"{quantity} devices connected:\n" +
                   "".join(f"mac: {device['mac']}, ip: {device['ip']} \n" for device in self.devices))
        return message


log = DhcpLogHandler('/var/log/syslog')
print(log.connected_devices())

