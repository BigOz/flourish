from datetime import datetime
BASE_RATE = 0.1075
OFF_PEAK_RATE = 0.01401
ON_PEAK_RATE = 0.04376

YEAR = 2016

class CostNN:
    def __init__(self):
        pass

    def get_prediction(self, time_of_day, day_of_year):
        day_of_week = self.get_day_of_week(YEAR, day_of_year, time_of_day)
        if (day_of_week < 5) and (13 < time_of_day) and (time_of_day < 20):
            return BASE_RATE + ON_PEAK_RATE
        else:
            return BASE_RATE - OFF_PEAK_RATE

    def get_day_of_week(self, YEAR, day_of_year, time_of_day):
        date_string = "{}-{}-{} MST".format(YEAR, day_of_year + 1, time_of_day)
        date = datetime.strptime(date_string, '%Y-%j-%H %Z')
        return date.weekday()

# base_rate taken from my current energy bill, peak pricing rates taken from
# https://www.rockymountainpower.net/ya/po/otou/utah/todf.html