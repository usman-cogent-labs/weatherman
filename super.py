import argparse
from DirectoryStream import DirectoryStream
from FileStream import FileStream
from Printer import Printer


parser = argparse.ArgumentParser(description='Process some files.')
parser.add_argument('-c', '--current', type=str, help='current year/month in YYYY/MM format')
parser.add_argument('-a', '--average', type=str, help='average year/month in YYYY/MM format')
parser.add_argument('-e', '--extreme', type=int, help='the year to filter files by')
args = parser.parse_args()


if __name__ == "__main__":
    if args.extreme:
        directory_stream = DirectoryStream(f'*_{args.extreme}_*')
        file_names = directory_stream.read()
        file_stream = FileStream()
        yearly_readings = file_stream.read(file_names)
        printer = Printer(yearly_readings)
        printer.print_yearly_readings()

    if args.average:
        monthly_readings = get_monthly_readings(args.average)
        print_monthly_average_readings(monthly_readings)
    if args.current:
        monthly_readings = get_monthly_readings(args.current)
        print_monthly_readings(monthly_readings)


