import pickle
import os.path
from predictors.nn_cost import CostNN
from predictors.home_profile import HomeProfile
from battery.battery import Battery
from battery.smart_battery import SmartBattery
from battery.no_battery import NoBattery
from state import State, Battery
from evaluator import Evaluator

SELL_BACK = False
DAYS_IN_YEAR = 366
HOURS_IN_DAY = 24

def main(solar_panels, smart_battery, smart_home, look_ahead_depth):
    print('About to run 1 year of simulations')
    print('Solar Panels = {}'.format(solar_panels))
    print('Smart Battery = {}'.format(smart_battery))
    print('Smart Appliances = {}'.format(smart_home))
    print('Look-ahead Depth = {}'.format(look_ahead_depth))

    predicted_solar = get_predicted_solar(solar_panels)
    actual_solar = get_actual_solar(solar_panels)

    predicted_cost = get_predicted_cost()
    actual_cost = get_actual_cost()

    home_profile = get_home_profile(smart_home)

    evaluator = Evaluator(predicted_solar, predicted_cost, home_profile, SELL_BACK)
    battery = get_battery(smart_battery, evaluator)

    output_file = setup_output_file(solar_panels, smart_battery, smart_home, look_ahead_depth)

    charge = 0.0
    for doy in range(0, 365):
        for tod in range(0, 24):
            state = State(charge, tod, doy, look_ahead_depth, 0.0)
            move = battery.get_action(state)
            cost = get_cost_of_move(move, state, home_profile, actual_solar, actual_cost, evaluator)
            charge = get_updated_charge(move, state, evaluator)
            output_entry = get_output_entry(doy, tod, move, cost, charge)
            output_file.write(output_entry)
    output_file.close()


def get_cost_of_move(move_choice, state, home_profile, actual_solar, actual_cost, evaluator):
    return evaluator.get_move_cost(move_choice, state, home_profile, actual_solar, actual_cost)


def get_updated_charge(move, state, evaluator):
    return evaluator.get_next_charge(move, state.battery)


def get_battery(smart_battery, evaluator):
    if smart_battery:
        return SmartBattery(evaluator)
    else:
        return NoBattery()


def get_predicted_solar(solar_panels):
    if solar_panels:
        pickled_predictions = open("src/2016_solar_predictions", "rb")
        predictions = pickle.load(pickled_predictions)
        return predictions
    else:
        prediction = list()
        for days in range(0,DAYS_IN_YEAR):
            daily_time = 24 * [0.0]
            prediction.append(daily_time)
        return prediction


def get_actual_solar(solar_panels):
    if solar_panels:
        pickled_actual = open("src/2016_solar_actual", "rb")
        actual = pickle.load(pickled_actual)
        return actual
    else:
        actual = list()
        for days in range(0, DAYS_IN_YEAR):
            daily_time = 24 * [0.0]
            actual.append(daily_time)
        return actual


def get_predicted_cost():
    cost_nn = CostNN()
    predicted_cost = list()
    for doy in range(0, DAYS_IN_YEAR):
        list_of_days = list()
        for tod in range(0, HOURS_IN_DAY):
            list_of_days.append(cost_nn.get_prediction(tod, doy))
        predicted_cost.append(list_of_days)
    return predicted_cost


def get_actual_cost():
    cost_nn = CostNN()
    predicted_cost = list()
    for doy in range(0, DAYS_IN_YEAR):
        list_of_days = list()
        for tod in range(0, HOURS_IN_DAY):
            list_of_days.append(cost_nn.get_prediction(tod, doy))
        predicted_cost.append(list_of_days)
    return predicted_cost


def get_home_profile(smart_home):
    home_profile = HomeProfile()
    return home_profile.get_usage(smart_home)


def setup_output_file(solar_panels, smart_battery, smart_home, look_ahead_depth):
    filename = get_filename(solar_panels, smart_battery, smart_home, look_ahead_depth)
    subdirectory = "simulation_data"
    try:
        os.mkdir(subdirectory)
    except Exception:
        pass
    print('\nAll simulations will be written to file "{}"\n'.format(filename))
    output_file = open(os.path.join(subdirectory, filename  + ".csv"), 'a')
    output_file.write('"Day of Year","Time of Day","Move Choice","Move Cost","Battery Charge"\n')
    return output_file


def get_output_entry(doy, tod, move, cost, charge):
    entry = "{},{},{},{},{}\n".format(doy, tod, move, cost, charge)
    return entry


def get_filename(solar_panels, smart_battery, smart_home, look_ahead_depth):
    filename = "{}_".format(look_ahead_depth)
    filename += get_letter(solar_panels)
    filename += get_letter(smart_battery)
    filename += get_letter(smart_home)
    return filename


def get_letter(boolean_value):
    if boolean_value:
        return "y"
    else:
        return "n"
