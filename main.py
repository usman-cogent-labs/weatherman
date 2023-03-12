import argparse
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
    data = list()
    for filename in weather_filenames:
        with open('weatherfiles/' + filename, 'r') as file_data:
            csvreader = csv.DictReader(file_data)
            records = list()
            for row in csvreader:
                raw_date = row['PKT'].split('-')
                year = int(raw_date[0])
                month = int(raw_date[1])
                day = int(raw_date[2])
                date = datetime.datetime(year, month, day)
                records.append({
                    "date": row['PKT'],
                    "highest_temperature": row['Max TemperatureC'],
                    "lowest_temperature": row['Min TemperatureC'],
                    "mean_humidity": row[' Mean Humidity'],
                    "max_humidity": row['Max Humidity'],
                })
            data.append({"month": date.strftime('%B'), "records": records})
    return data


def get_formatted_date(date):
    year, month, day = date.split('-')
    return datetime.date(int(year), int(month), int(day)).strftime('%B %d')


def print_yearly_data(data):
    highest = {"temperature": 0, "date": ''}
    lowest = {"temperature": 1000, "date": ''}
    humidest = {"temperature": 0, "date": ''}

    for month_data in data:
        for record in month_data['records']:
            if record['highest_temperature'].isnumeric() \
                    and int(record['highest_temperature']) > highest['temperature']:
                highest['temperature'] = int(record['highest_temperature'])
                highest['date'] = get_formatted_date(record['date'])
            if record['lowest_temperature'].isnumeric() and int(record['lowest_temperature']) < lowest['temperature']:
                lowest["temperature"] = int(record['lowest_temperature'])
                lowest['date'] = get_formatted_date(record['date'])
            if record['max_humidity'].isnumeric() and int(record['max_humidity']) > humidest['temperature']:
                humidest['temperature'] = int(record['max_humidity'])
                humidest['date'] = get_formatted_date(record['date'])
    print(f"Highest: {highest['temperature']}C on {highest['date']}")
    print(f"Lowest: {lowest['temperature']}C on {lowest['date']}")
    print(f"Humidity: {humidest['temperature']}% on {humidest['date']}")


def check_month_in_command(command_data):
    return False if len(command_data.split('/')) == 1 else True


def get_month_data_from_data(data, month):
    return next((item for item in data if item["month"] == month), None)


def print_monthly_average_data(data, command_data):
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
    for record in data['records']:
        if record['highest_temperature'] != '':
            highest_temp_data['sum'] += int(record['highest_temperature'])
            highest_temp_data["count"] += 1
        if record['lowest_temperature'] != '':
            lowest_temp_data["sum"] += int(record['lowest_temperature'])
            lowest_temp_data["count"] += 1
        if record['mean_humidity'] != '':
            humidity_temp_data["sum"] += int(record['mean_humidity'])
            humidity_temp_data["count"] += 1

    highest_average = highest_temp_data["sum"] // highest_temp_data["count"]
    lowest_average = lowest_temp_data["sum"] // lowest_temp_data["count"]
    average_humidity = humidity_temp_data["sum"] // humidity_temp_data["count"]

    print(f'Highest Average: {highest_average}')
    print(f'Lowest Average: {lowest_average}')
    print(f'Average Mean Humidity: {average_humidity}')


def draw_month_graph(data, month):
    print(get_month_data_from_data(data, month))


def get_year_month_from_command(command_data):
    if not check_month_in_command(command_data):
        return command_data
    year, month = command_data.split('/')
    month = calendar.month_name[int(month)]
    return year, month


def get_yearly_data(files, command_data):
    if len(get_year_month_from_command(command_data)) == 2:
        year, month = get_year_month_from_command(command_data)
    else:
        year = get_year_month_from_command(command_data)
    file_names = get_year_file_names(files, year)
    file_data = parse_weather_files(file_names)
    return file_data


def get_monthly_data(files, command_data):
    year, month = get_year_month_from_command(command_data)
    yearly_data = get_yearly_data(files, command_data)
    monthly_data = get_month_data_from_data(yearly_data, month)
    return monthly_data


def print_monthly_data(monthly_data):
    for record in monthly_data["records"]:
        if bool(record["highest_temperature"]) is True:
            print(Fore.RED + "+" * int(record["highest_temperature"]), record["highest_temperature"] + "C")
        if bool(record["lowest_temperature"]) is True:
            print(Fore.BLUE + "+" * int(record["lowest_temperature"]), record["lowest_temperature"] + "C")
    print(Style.RESET_ALL)


def get_files_from_directory():
    return os.listdir('weatherfiles/')


def execute_command(command_type, command_data):
    files = get_files_from_directory()
    if command_type == "-e":
        yearly_data = get_yearly_data(files, command_data)
        print_yearly_data(yearly_data)
    if command_type == "-a":
        monthly_data = get_monthly_data(files, command_data)
        print_monthly_average_data(monthly_data, command_data)
    if command_type == "-c":
        monthly_data = get_monthly_data(files, command_data)
        print_monthly_data(monthly_data)


if __name__ == "__main__":
    for parameter in range(1, len(sys.argv), 2):
        execute_command(sys.argv[parameter], sys.argv[parameter + 1])

