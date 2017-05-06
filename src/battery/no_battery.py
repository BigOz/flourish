from battery.battery import Battery

class NoBattery(Battery):
    def __init__(self):
        pass

    def get_action(self, current_state):
        return "no_battery"