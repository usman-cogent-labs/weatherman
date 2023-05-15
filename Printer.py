import datetime


class Printer:
    def __init__(self, readings):
        self.readings = readings

    def __get_formatted_date(self, date):
        year, month, day = date.split("-")

        return datetime.date(int(year), int(month), int(day)).strftime("%B %d")

    def __print_red(self, str):
        print("\033[91m {}\033[00m".format(str))

    def __print_blue(self, str):
        print("\033[34m {}\033[00m".format(str))

    def __get_attribute_sum_from_weather_records(self, records, attribute):
        return sum(int(record[attribute]) for record in records if record[attribute] != '')

    def __count_non_empty_attribute_readings(self, records, attribute):
        return sum(1 for record in records if record[attribute] != '')

    def print_yearly_readings(self):
        highest = {"temperature": 0, "date": ""}
        lowest = {"temperature": 1000, "date": ""}
        humidest = {"temperature": 0, "date": ""}

        for monthly_readings in self.readings:
            for record in monthly_readings["records"]:
                if record["highest_temperature"].isnumeric() \
                        and int(record["highest_temperature"]) > highest["temperature"]:
                    highest["temperature"] = int(record["highest_temperature"])
                    highest["date"] = self.__get_formatted_date(record["date"])
                if record["lowest_temperature"].isnumeric() \
                        and int(record["lowest_temperature"]) < lowest["temperature"]:
                    lowest["temperature"] = int(record["lowest_temperature"])
                    lowest["date"] = self.__get_formatted_date(record["date"])
                if record["max_humidity"].isnumeric() \
                        and int(record["max_humidity"]) > humidest["temperature"]:
                    humidest["temperature"] = int(record["max_humidity"])
                    humidest["date"] = self.__get_formatted_date(record["date"])

        print(f"Highest: {highest['temperature']}C on {highest['date']}")
        print(f"Lowest: {lowest['temperature']}C on {lowest['date']}")
        print(f"Humidity: {humidest['temperature']}% on {humidest['date']}")

    def print_monthly_readings(self):
        for monthly_reading in self.readings:
            for record in monthly_reading["records"]:
                if bool(record["highest_temperature"]):
                    self.__print_red(f"{'+' * int(record['highest_temperature'])} {record['highest_temperature']} C")
                if bool(record["lowest_temperature"]):
                    self.__print_blue(f"{'+' * int(record['lowest_temperature'])} {record['lowest_temperature']} C")

    def print_monthly_average_readings(self):
        records = self.readings[0]['records']
        print(
            f"Highest Average: {self.__get_attribute_sum_from_weather_records(records, 'highest_temperature') // self.__count_non_empty_attribute_readings(records, 'highest_temperature')}")
        print(
            f"Lowest Average: {self.__get_attribute_sum_from_weather_records(records, 'lowest_temperature') // self.__count_non_empty_attribute_readings(records, 'lowest_temperature')}")
        print(
            f"Average Mean Humidity: {self.__get_attribute_sum_from_weather_records(records, 'mean_humidity') // self.__count_non_empty_attribute_readings(records, 'mean_humidity')}")