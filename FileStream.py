import csv
import datetime
from Stream import Stream


class FileStream(Stream):
    def read(self, weather_filenames):
        readings = []
        for filename in weather_filenames:
            with open(filename, "r") as weather_file:
                weather_readings = csv.DictReader(weather_file)
                records = []

                for row in weather_readings:
                    raw_date = row["PKT"].split("-")
                    year, month, day = int(raw_date[0]), int(raw_date[1]), int(raw_date[2])
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
