import math
from time import sleep

from docker import Client
from rpi_lcd import LCD


class SwarmInfo(object):

    def __init__(self):
        self.client = Client(base_url='unix://var/run/docker.sock')

    def is_manager(self):
        return self.client.info()['Swarm']['ControlAvailable']

    def get_nodes(self):
        return [node for node in self.client.nodes()
                if node['Status']['State'] == 'ready']

    def get_node_by_role(self, role):
        return [node for node in self.get_nodes()
                if node['Spec']['Role'] == role]

    def get_managers(self):
        return self.get_node_by_role('manager')

    def get_workers(self):
        return self.get_node_by_role('worker')

    def get_total_memory(self):
        return self._size_format(sum(
            [node['Description']['Resources']['MemoryBytes']
             for node in self.get_nodes()]) / 1024)

    def get_running_tasks(self):
        return self.client.tasks(filters={'desired-state': 'running'})

    def get_node_ip(self):
        return self.client.info()['Swarm']['NodeAddr']

    def _size_format(self, size):
        unit = ("KB", "MB", "GB")
        i = int(math.floor(math.log(size, 1024)))
        s = round(size / math.pow(1024, i), 2)
        return '%s %s' % (s, unit[i])


def main():
    lcd = LCD()
    swarm = SwarmInfo()

    while True:
        sleep(1)
        if not swarm.is_manager():
            lcd.text('Swarm is disabled', 1)
        else:
            managers = len(swarm.get_managers())
            workers = len(swarm.get_workers())
            lcd.text('%s manager, %s worker%s' % (
                managers, workers, '' if workers == 1 else 's'), 1)
            lcd.text('IP: %s' % (swarm.get_node_ip(),), 2)
            lcd.text('Memory: %s' % (swarm.get_total_memory(),), 3)
            lcd.text('Running tasks: %s' % (len(swarm.get_running_tasks())), 4)


if __name__ == "__main__":
    main()
