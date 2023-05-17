class Calculator:
    def __get_non_empty_value(self, value, infinity_value):
        if value and value.isdigit():
            return int(value)
        return float(infinity_value)

    def __get_attribute_sum_from_weather_records(self, records, attribute):
        return sum(int(record[attribute]) for record in records if record[attribute] != "")

    def __count_non_empty_attribute_readings(self, records, attribute):
        return sum(1 for record in records if record[attribute] != "")

    def calculate_year_weather_readings(self, weather_readings):
        coldest_day = min(min(weather_readings,
                              key=lambda x: max(int(record["lowest_temperature"]) for record
                                                in x["records"]
                                                if record["lowest_temperature"].isdigit()))["records"],
                          key=lambda weather_record: self.__get_non_empty_value(weather_record[
                                                                                    "lowest_temperature"], "+inf"))
        hottest_day = max(max(weather_readings,
                              key=lambda x: max(int(record["highest_temperature"]) for record
                                                in x["records"]
                                                if record["highest_temperature"].isdigit()))["records"],
                          key=lambda weather_record: self.__get_non_empty_value(weather_record[
                                                                                    "highest_temperature"], "-inf"))
        humid_day = max(max(weather_readings,
                            key=lambda x: max(int(record["max_humidity"]) for record
                                              in x["records"]
                                              if record["max_humidity"].isdigit()))["records"],
                        key=lambda weather_record: self.__get_non_empty_value(weather_record[
                                                                                  "max_humidity"], "-inf"))
        return {
            "hottest_day": {"temperature": hottest_day["highest_temperature"], "date": hottest_day["date"]},
            "coldest_day": {"temperature": coldest_day["lowest_temperature"], "date": coldest_day["date"]},
            "humid_day": {"temperature": humid_day["max_humidity"], "date": coldest_day["date"]},
        }

    def calculate_monthly_average_readings(self, weather_records):
        return {
            "highest_average": self.__get_attribute_sum_from_weather_records(weather_records, "highest_temperature") //
                               self.__count_non_empty_attribute_readings(weather_records, "highest_temperature"),
            "lowest_average": self.__get_attribute_sum_from_weather_records(weather_records, "lowest_temperature") //
                              self.__count_non_empty_attribute_readings(weather_records, "lowest_temperature"),
            "average_mean_humidity": self.__get_attribute_sum_from_weather_records(weather_records, "mean_humidity") //
                                     self.__count_non_empty_attribute_readings(weather_records, "mean_humidity")
        }
