import argparse
import csv
import calendar
from colorama import Fore, Style
import datetime
import glob
import os


parser = argparse.ArgumentParser(description='Process some files.')
parser.add_argument('-c', '--current', type=str, help='current year/month in YYYY/MM format')
parser.add_argument('-a', '--average', type=str, help='average year/month in YYYY/MM format')
parser.add_argument('-e', '--extreme', type=int, help='the year to filter files by')
args = parser.parse_args()


def parse_weather_files(weather_filenames):
    readings = []
    for filename in weather_filenames:
        with open(filename, "r") as weather_file:
            weather_readings = csv.DictReader(weather_file)
            records = []

            for row in weather_readings:
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


def print_monthly_average_readings(monthly_readings):
    highest_temp_data = {
        "sum": 0,
        "count": 0
    }
    lowest_temp_data = {
        "sum": 0,
        "count": 0
    }
    humidity_temp_data = {
        "sum": 0,
        "count": 0
    }

    for monthly_reading in monthly_readings:
        for record in monthly_reading["records"]:
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


def print_monthly_readings(monthly_readings):
    for record in monthly_readings["records"]:
        if bool(record["highest_temperature"]):
            print(f"{Fore.RED} {'+' * int(record['highest_temperature'])} {record['highest_temperature']} C")
        if bool(record["lowest_temperature"]):
            print(f"{Fore.BLUE} {'+' * int(record['lowest_temperature'])} {record['lowest_temperature']} C")

    print(Style.RESET_ALL)


def get_file_names(file_path):
    return glob.glob(os.path.join('weatherfiles/', f'*_{file_path}_*'))


def get_monthly_readings(command_type):
    year, month = command_type.split('/')
    month_name = calendar.month_name[int(month)][:3]
    return parse_weather_files(get_file_names(f'{year}_{month_name}'))


def execute_command():
    if args.extreme:
        file_names = glob.glob(os.path.join('weatherfiles/', f'*_{args.extreme}_*'))
        yearly_readings = parse_weather_files(file_names)
        print_yearly_readings(yearly_readings)
    if args.average:
        monthly_readings = get_monthly_readings(args.average)
        print_monthly_average_readings(monthly_readings)
    if args.current:
        monthly_readings = get_monthly_readings(args.current)
        print_monthly_readings(monthly_readings)


if __name__ == "__main__":
    execute_command()

