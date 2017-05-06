from state import State, Battery

class Evaluator:
    def __init__(self, predicted_solar, predicted_cost, home_profile, sell_back):
        self.solar_nn = predicted_solar
        self.cost_nn = predicted_cost
        self.home_profile = home_profile
        self.sell_back = sell_back

    def get_legal_moves(self, current_state):
        legal_moves = ["idle"]
        remaining_charge = current_state.battery.charge * current_state.battery.capacity
        remaining_capacity = current_state.battery.capacity - remaining_charge
        for i in range(1,11):
            if remaining_charge >= current_state.battery.rate * i * 0.1:
                legal_moves.append("d{}".format(i * 10))
            if remaining_capacity >= current_state.battery.rate * i * 0.1:
                legal_moves.append("c{}".format(i * 10))
        return legal_moves

    def get_updated_state(self, current_state, move_choice):
        tod = self.__get_next_time(current_state.time_of_day)
        doy = self.__get_next_day(current_state.day_of_year)
        charge = self.get_next_charge(move_choice, current_state.battery)
        rounds_remaining = current_state.rounds_remaining - 1
        cost = self.get_move_cost(move_choice, current_state, self.home_profile, self.solar_nn, self.cost_nn)
        return State(charge, tod, doy, rounds_remaining, current_state.cost + cost)

    def __get_next_time(self, current_time):
        if current_time == 23:
            return 0
        else:
            return current_time + 1

    def __get_next_day(self, current_day):
        if current_day == 365:
            return 1
        else:
            return current_day + 1

    def get_next_charge(self, move_choice, battery):
        if move_choice == "idle":
            return battery.charge
        elif move_choice[0] == "c":
            additional_charge = float(move_choice[1:]) / 100 * battery.rate
            percent_to_add = additional_charge / battery.capacity
            return battery.charge + percent_to_add
        elif move_choice[0] == "d":
            additional_discharge = float(move_choice[1:]) / 100 * battery.rate
            percent_to_remove = additional_discharge / battery.capacity
            return battery.charge - percent_to_remove

    def get_move_cost(self, move_choice, current_state, home_profile, solar_nn, cost_nn):
        current_usage = home_profile[current_state.time_of_day]
        current_usage -= solar_nn[current_state.day_of_year][current_state.time_of_day]
        if move_choice[0] == "c":
            current_usage += float(move_choice[1:]) / 100 * current_state.battery.rate
        elif move_choice[0] == "d":
            current_usage -= float(move_choice[1:]) / 100 * current_state.battery.rate
        move_cost = current_usage * cost_nn[current_state.day_of_year][current_state.time_of_day] / 1000
        if move_cost < 0 and self.sell_back is False:
            move_cost = 0
        return move_cost