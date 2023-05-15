import argparse
from DirectoryStream import DirectoryStream
from FileStream import FileStream
from Helpers import Helpers
from Printer import Printer


parser = argparse.ArgumentParser(description='Process some files.')
parser.add_argument('-c', '--current', type=str, help='current year/month in YYYY/MM format')
parser.add_argument('-a', '--average', type=str, help='average year/month in YYYY/MM format')
parser.add_argument('-e', '--extreme', type=int, help='the year to filter files by')
args = parser.parse_args()


def get_weather_readings(file_path):
    directory_stream = DirectoryStream(file_path)
    file_names = directory_stream.read()
    file_stream = FileStream(file_names)
    readings = file_stream.read()

    return readings


if __name__ == "__main__":
    if args.extreme:
        yearly_readings = get_weather_readings(f'*_{args.extreme}_*')
        printer = Printer(yearly_readings)
        printer.print_yearly_readings()

    if args.average:
        monthly_readings = get_weather_readings(Helpers.get_monthly_readings(args.average))
        printer = Printer(monthly_readings)
        printer.print_monthly_average_readings()
    if args.current:
        monthly_readings = get_weather_readings(Helpers.get_monthly_readings(args.current))
        printer = Printer(monthly_readings)
        printer.print_monthly_readings()


