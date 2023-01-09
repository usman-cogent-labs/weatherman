import os
import sys
import datetime

LOWEST_TEMPERATURE = 'Min TemperatureC'
HIGHEST_TEMPERATURE = 'Max TemperatureC'
MEAN_HUMIDITY_TEMPERATURE = 'Mean Humidity'
MAX_HUMIDITY_TEMPERATURE = 'Max Humidity'
MONTHS = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'

}


def get_files_from_drectory():
    return os.listdir('weatherfiles/')


def get_year_file_names(files, year):
    year_files = []
    for file in files:
        if year in file:
            year_files.append(file)
    return year_files


def trim_list_elements(arr):
    stripped_elements = []
    for element in arr:
        stripped_elements.append(element.strip())
    return stripped_elements


def get_parameter_indexes(arr):
    return dict(
        highest_temp_index=arr.index(HIGHEST_TEMPERATURE),
        lowest_temp_index=arr.index(LOWEST_TEMPERATURE),
        mean_humidity_index=arr.index(MEAN_HUMIDITY_TEMPERATURE),
        max_humidity_index=arr.index(MAX_HUMIDITY_TEMPERATURE)
    )


def parse_files(filenames):
    data = list()
    for filename in filenames:
        file = open('weatherfiles/' + filename, 'r')
        line = file.readline()
        arr = line.split(',')
        arr = trim_list_elements(arr)
        indexes = get_parameter_indexes(arr)
        records = list()
        for line in file:
            line_elements = line.split(',')
            trimmed_elements = trim_list_elements(line_elements)
            raw_date = trimmed_elements[0].split('-')
            year = int(raw_date[0])
            month = int(raw_date[1])
            day = int(raw_date[2])
            date = datetime.datetime(year, month, day)
            records.append({
                "date": trimmed_elements[0],
                "highest_temperature": trimmed_elements[indexes['highest_temp_index']],
                "lowest_temperature": trimmed_elements[indexes['lowest_temp_index']],
                "mean_humidity": trimmed_elements[indexes['mean_humidity_index']],
                "max_humidity": trimmed_elements[indexes['max_humidity_index']],
            })
        data.append({"month": date.strftime('%B'), "records": records})
    return data


def get_year_values(data):
    highest = {"temperature": 0, "date": ''}
    lowest = {"temperature": 1000, "date": ''}
    humidest = {"temperature": 0, "date": ''}

    for month_data in data:
        for record in month_data['records']:
            if record['highest_temperature'].isnumeric() \
                    and int(record['highest_temperature']) > highest['temperature']:
                highest['temperature'] = int(record['highest_temperature'])
                highest['date'] = record['date']
            if record['lowest_temperature'].isnumeric() and int(record['lowest_temperature']) < lowest['temperature']:
                lowest["temperature"] = int(record['lowest_temperature'])
                lowest['date'] = record['date']
            if record['max_humidity'].isnumeric() and int(record['max_humidity']) > humidest['temperature']:
                humidest['temperature'] = int(record['max_humidity'])
                humidest['date'] = record['date']
    highest_date = highest['date'].split('-')
    lowest_date = lowest['date'].split('-')
    humidest_date = humidest['date'].split('-')
    print(
        f"Highest: {highest['temperature']}C on {datetime.datetime(int(highest_date[0]), int(highest_date[1]), int(highest_date[2])).strftime('%B %d')}")
    print(
        f"Lowest: {lowest['temperature']}C on {datetime.datetime(int(lowest_date[0]), int(lowest_date[1]), int(lowest_date[2])).strftime('%B %d')}")
    print(
        f"Humidity: {humidest['temperature']}% on {datetime.datetime(int(humidest_date[0]), int(humidest_date[1]), int(humidest_date[2])).strftime('%B %d')}")


def check_command_month(data):
    data = data.split('/')
    if int(data[1]) > max(MONTHS.keys()) or int(data[1]) < min(MONTHS.keys()):
        return -1
    elif MONTHS[int(data[1])]:
        return MONTHS[int(data[1])]
    else:
        return -1


def check_month_in_command(data):
    data = data.split('/')
    if len(data) == 1:
        return False
    else:
        return True


if __name__ == '__main__':
    if len(sys.argv) > 2:
        command_type = sys.argv[1]
        all_files = get_files_from_drectory()
        if command_type == '-e':
            file_names = get_year_file_names(all_files, sys.argv[2])
            file_data = parse_files(file_names)
            get_year_values(file_data)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
