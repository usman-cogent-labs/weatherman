import csv
import calendar
from colorama import Fore, Style
import datetime
import os
import sys


def get_year_file_names(weather_reports, year):
    return [weather_report for weather_report in weather_reports if year in weather_report]


def trim_list_elements(arr):
    return [element.strip() for element in arr]


def parse_weather_files(weather_filenames):
    readings = list()
    for filename in weather_filenames:
        with open("weatherfiles/" + filename, "r") as file_data:
            csvreader = csv.DictReader(file_data)
            records = list()

            for row in csvreader:
                raw_date = row["PKT"].split("-")
                year = int(raw_date[0])
                month = int(raw_date[1])
                day = int(raw_date[2])
                date = datetime.datetime(year, month, day)
                records.append({
                    "date": row["PKT"],
                    "highest_temperature": row["Max TemperatureC"],
                    "lowest_temperature": row["Min TemperatureC"],
                    "mean_humidity": row[" Mean Humidity"],
                    "max_humidity": row["Max Humidity"],
                })
            readings.append({"month": date.strftime("%B"), "records": records})

    return readings


def get_formatted_date(date):
    year, month, day = date.split("-")
    return datetime.date(int(year), int(month), int(day)).strftime("%B %d")


def print_yearly_readings(readings):
    highest = {"temperature": 0, "date": ""}
    lowest = {"temperature": 1000, "date": ""}
    humidest = {"temperature": 0, "date": ""}

    for monthly_readings in readings:
        for record in monthly_readings["records"]:
            if record["highest_temperature"].isnumeric() \
                    and int(record["highest_temperature"]) > highest["temperature"]:
                highest["temperature"] = int(record["highest_temperature"])
                highest["date"] = get_formatted_date(record["date"])
            if record["lowest_temperature"].isnumeric() and int(record["lowest_temperature"]) < lowest["temperature"]:
                lowest["temperature"] = int(record["lowest_temperature"])
                lowest["date"] = get_formatted_date(record["date"])
            if record["max_humidity"].isnumeric() and int(record["max_humidity"]) > humidest["temperature"]:
                humidest["temperature"] = int(record["max_humidity"])
                humidest["date"] = get_formatted_date(record["date"])

    print(f"Highest: {highest['temperature']}C on {highest['date']}")
    print(f"Lowest: {lowest['temperature']}C on {lowest['date']}")
    print(f"Humidity: {humidest['temperature']}% on {humidest['date']}")


def check_month_in_command(command_line_arguments):
    return False if len(command_line_arguments.split("/")) == 1 else True


def get_monthly_readings_from_yearly_readings(yearly_readings, month):
    return next((item for item in yearly_readings if item["month"] == month), None)


def print_monthly_average_readings(data):
    highest_temp_data = {
        "sum": 0,
        "count": 0,
    }
    lowest_temp_data = {
        "sum": 0,
        "count": 0,
    }
    humidity_temp_data = {
        "sum": 0,
        "count": 0
    }
    for record in data["records"]:
        if record["highest_temperature"] != "":
            highest_temp_data["sum"] += int(record["highest_temperature"])
            highest_temp_data["count"] += 1
        if record["lowest_temperature"] != "":
            lowest_temp_data["sum"] += int(record["lowest_temperature"])
            lowest_temp_data["count"] += 1
        if record["mean_humidity"] != "":
            humidity_temp_data["sum"] += int(record["mean_humidity"])
            humidity_temp_data["count"] += 1

    highest_average = highest_temp_data["sum"] // highest_temp_data["count"]
    lowest_average = lowest_temp_data["sum"] // lowest_temp_data["count"]
    average_humidity = humidity_temp_data["sum"] // humidity_temp_data["count"]

    print(f"Highest Average: {highest_average}")
    print(f"Lowest Average: {lowest_average}")
    print(f"Average Mean Humidity: {average_humidity}")


def get_year_month_from_command(command_line_arguments):
    if not check_month_in_command(command_line_arguments):
        return command_line_arguments

    year, month = command_line_arguments.split("/")
    month = calendar.month_name[int(month)]

    return year, month


def get_yearly_readings(files, command_line_arguments):
    year, month = get_year_month_from_command(command_line_arguments)\
        if len(get_year_month_from_command(command_line_arguments)) == 2\
        else (get_year_month_from_command(command_line_arguments), None)
    file_names = get_year_file_names(files, year)
    return parse_weather_files(file_names)


def get_monthly_weather_readings(files, command_line_arguments):
    year, month = get_year_month_from_command(command_line_arguments)
    yearly_readings = get_yearly_readings(files, command_line_arguments)
    return get_monthly_readings_from_yearly_readings(yearly_readings, month)


def print_monthly_readings(monthly_readings):
    for record in monthly_readings["records"]:
        if bool(record["highest_temperature"]) is True:
            print(f"{Fore.RED} {'+' * int(record['highest_temperature'])} {record['highest_temperature']} C")
        if bool(record["lowest_temperature"]) is True:
            print(f"{Fore.BLUE} {'+' * int(record['lowest_temperature'])} {record['lowest_temperature']} C")

    print(Style.RESET_ALL)


def get_files_from_directory():
    return os.listdir("weatherfiles/")


def execute_command(command_type, command_line_arguments):
    files = get_files_from_directory()
    match command_type:
        case "-e":
            yearly_readings = get_yearly_readings(files, command_line_arguments)
            print_yearly_readings(yearly_readings)
        case "-a":
            monthly_readings = get_monthly_weather_readings(files, command_line_arguments)
            print_monthly_average_readings(monthly_readings)
        case "-c":
            monthly_readings = get_monthly_weather_readings(files, command_line_arguments)
            print_monthly_readings(monthly_readings)


if __name__ == "__main__":
    for parameter in range(1, len(sys.argv), 2):
        execute_command(sys.argv[parameter], sys.argv[parameter + 1])

