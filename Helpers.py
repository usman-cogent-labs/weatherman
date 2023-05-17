import calendar


class Helpers:
    @staticmethod
    def get_year_month_from_command(command_type):
        year, month = command_type.split('/')
        month_name = calendar.month_name[int(month)][:3]
        return f'*_{year}_{month_name}*'
