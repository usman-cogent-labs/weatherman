import argparse
from DirectoryStream import DirectoryStream
from FileStream import FileStream
from Helpers import Helpers
from Printer import Printer


class Driver:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Process some files.')
        parser.add_argument('-c', '--current', type=str, help='current year/month in YYYY/MM format')
        parser.add_argument('-a', '--average', type=str, help='average year/month in YYYY/MM format')
        parser.add_argument('-e', '--extreme', type=int, help='the year to filter files by')
        self.args = parser.parse_args()

    def run(self):
        directory_stream = DirectoryStream()
        file_stream = FileStream()
        if self.args.extreme:
            file_names = directory_stream.read(f'*_{self.args.extreme}_*')
            yearly_readings = file_stream.read(file_names)
            printer = Printer(yearly_readings)
            printer.print_yearly_readings()
        if self.args.average:
            file_names = directory_stream.read(Helpers.get_year_month_from_command(self.args.average))
            monthly_readings = file_stream.read(file_names)
            printer = Printer(monthly_readings)
            printer.print_monthly_average_readings()
        if self.args.current:
            file_names = directory_stream.read(Helpers.get_year_month_from_command(self.args.current))
            monthly_readings = file_stream.read(file_names)
            printer = Printer(monthly_readings)
            printer.print_monthly_readings()
