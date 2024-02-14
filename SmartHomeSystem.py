from abc import ABC, abstractmethod
from datetime import datetime
import json


# Observer Pattern
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass


class Device(Observer):
    def __init__(self, device_id, device_type):
        self.device_id = device_id
        self.device_type = device_type
        self.status = None

    @abstractmethod
    def display_status(self):
        pass


# Concrete Observers
class Light(Device):
    def update(self, message):
        self.status = message
        self.display_status()

    def display_status(self):
        print(f"Light {self.device_id} is {self.status}.")


class Thermostat(Device):
    def update(self, message):
        self.status = f"set to {message} degrees"
        self.display_status()

    def display_status(self):
        print(f"Thermostat is {self.status}.")


class DoorLock(Device):
    def update(self, message):
        self.status = message
        self.display_status()

    def display_status(self):
        print(f"Door is {self.status}.")


# Proxy Pattern
class DeviceProxy:
    def __init__(self, real_device):
        self._real_device = real_device

    def __getattr__(self, attr):
        print(f"Accessing {attr} of {self._real_device.device_type} {self._real_device.device_id} through Proxy.")
        return getattr(self._real_device, attr)


# Factory Method
class DeviceFactory:
    def create_device(self, device_info):
        device_id = device_info['id']
        device_type = device_info['type']

        if device_type == 'light':
            return Light(device_id, device_type)
        elif device_type == 'thermostat':
            return Thermostat(device_id, device_type)
        elif device_type == 'door':
            return DoorLock(device_id, device_type)


# Smart Home System
class SmartHomeSystem:
    def __init__(self):
        self.devices = []
        self.scheduled_tasks = []
        self.triggers = []

    def add_device(self, device_info):
        factory = DeviceFactory()
        device = factory.create_device(device_info)
        self.devices.append(DeviceProxy(device))

    def turn_on(self, device_id):
        for device in self.devices:
            if device._real_device.device_id == device_id:
                device._real_device.update('On')
                break

    def turn_off(self, device_id):
        for device in self.devices:
            if device._real_device.device_id == device_id:
                device._real_device.update('Off')
                break

    def set_schedule(self, device_id, time, command):
        self.scheduled_tasks.append({'device': device_id, 'time': time, 'command': command})

    def add_trigger(self, condition, action):
        self.triggers.append({'condition': condition, 'action': action})

    def execute_scheduled_tasks(self, current_time):
        for task in self.scheduled_tasks:
            if current_time.strftime("%H:%M") == task['time']:
                self.execute_command(task['device'], task['command'])

    def execute_triggers(self, condition):
        for trigger in self.triggers:
            if eval(condition + trigger['condition']):
                self.execute_command(trigger['action']['device'], trigger['action']['command'])

    def execute_command(self, device_id, command):
        if 'turnOn' in command:
            self.turn_on(device_id)
        elif 'turnOff' in command:
            self.turn_off(device_id)

    def display_status_report(self):
        for device in self.devices:
            device._real_device.display_status()
        print(f"Scheduled Tasks: {json.dumps(self.scheduled_tasks)}")
        print(f"Automated Triggers: {json.dumps(self.triggers)}")


# Client code
if __name__ == "__main__":
    smart_home = SmartHomeSystem()

    devices_info = [
        {'id': 1, 'type': 'light'},
        {'id': 2, 'type': 'thermostat'},
        {'id': 3, 'type': 'door'}
    ]

    for device_info in devices_info:
        smart_home.add_device(device_info)

    smart_home.set_schedule(1, "06:00", "turnOn(1)")
    smart_home.add_trigger("temperature > 75", {'device': 1, 'command': 'turnOff(1)'})

    current_time = datetime.strptime("06:00", "%H:%M")
    smart_home.execute_scheduled_tasks(current_time)

    temperature_condition = 80
    smart_home.execute_triggers(f"temperature == {temperature_condition}")

    smart_home.display_status_report()
