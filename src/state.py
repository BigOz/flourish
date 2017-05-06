class State:
    def __init__(self, charge, time_of_day, day_of_year, rounds_remaining, cost):
        self.battery = Battery(charge)
        self.time_of_day = time_of_day
        self.day_of_year = day_of_year
        self.rounds_remaining = rounds_remaining
        self.cost = cost

class Battery:
    def __init__(self, charge):
        self.capacity = 13500
        self.charge = charge
        self.rate = 5000