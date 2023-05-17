from Calculator import Calculator
import datetime


class Printer:
    def __init__(self, readings):
        self.readings = readings
        self.calculator = Calculator()

    def __get_formatted_date(self, date):
        year, month, day = date.split("-")

        return datetime.date(int(year), int(month), int(day)).strftime("%B %d")

    def __print_red(self, str):
        print("\033[91m {}\033[00m".format(str))

    def __print_blue(self, str):
        print("\033[34m {}\033[00m".format(str))

    def print_yearly_readings(self):
        yearly_weather_calculations = self.calculator.calculate_year_weather_readings(self.readings)
        print(
            f"Highest: {yearly_weather_calculations['hottest_day']['temperature']}C on "
            f"{self.__get_formatted_date(yearly_weather_calculations['hottest_day']['date'])}")
        print(
            f"Lowest: {yearly_weather_calculations['coldest_day']['temperature']}C on "
            f"{self.__get_formatted_date(yearly_weather_calculations['coldest_day']['date'])}")
        print(
            f"Humidity: {yearly_weather_calculations['humid_day']['temperature']}C on "
            f"{self.__get_formatted_date(yearly_weather_calculations['humid_day']['date'])}")

    def print_monthly_readings(self):
        for monthly_reading in self.readings:
            for record in monthly_reading["records"]:
                if bool(record["highest_temperature"]):
                    self.__print_red(f"{'+' * int(record['highest_temperature'])} {record['highest_temperature']} C")
                if bool(record["lowest_temperature"]):
                    self.__print_blue(f"{'+' * int(record['lowest_temperature'])} {record['lowest_temperature']} C")

    def print_monthly_average_readings(self):
        monthly_average_readings = self.calculator.calculate_monthly_average_readings(self.readings[0]['records'])
        print(
            f"Highest Average: {monthly_average_readings['highest_average']}")
        print(
            f"Lowest Average: {monthly_average_readings['lowest_average']}")
        print(
            f"Average Mean Humidity: {monthly_average_readings['average_mean_humidity']}")
