from csv import reader
from typing import List
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking
from domain.aggregated_data import AggregatedData


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str, rows_to_return: int = 5) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.rows_to_return = rows_to_return
        self.accelerometer_data_reader = None
        self.gps_data_reader = None
        self.parking_data_reader = None

    def fileDataReader(self, path: str):
        while True:
            with open(path) as file:
                data_reader = reader(file)
                header = next(data_reader)
                for row in data_reader:
                    yield row

    def read(self) -> List[AggregatedData]:
        """Method returns data obtained from sensors"""
        dataList = []
        for i in range(self.rows_to_return):
            parking_data = next(self.parking_data_reader)
            dataList.append(
                AggregatedData(
                    Accelerometer(*next(self.accelerometer_data_reader)),
                    Gps(*next(self.gps_data_reader)),
                    Parking(parking_data[0], parking_data[1:]),
                    datetime.now()
                )
            )
        return dataList

    def startReading(self):
        """Method should be called before starting to read data"""
        self.accelerometer_data_reader = self.fileDataReader(self.accelerometer_filename)
        self.gps_data_reader = self.fileDataReader(self.gps_filename)
        self.parking_data_reader = self.fileDataReader(self.parking_filename)

