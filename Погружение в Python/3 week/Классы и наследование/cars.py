import csv
import os


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)
        self.car_type = "car"

    def passenger_seats_count(self):
        return self.passenger_seats_count


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = "truck"
        body_args = body_whl.split('x')

        try:
            if len(body_args) != 3:
                raise ValueError
            for arg in body_args:
                if not float(arg):
                    raise ValueError
        except ValueError:
            self.body_length = 0.0
            self.body_width = 0.0
            self.body_height = 0.0
        else:
            self.body_length = float(body_args[0])
            self.body_width = float(body_args[1])
            self.body_height = float(body_args[2])

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra
        self.car_type = "spec_machine"


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)
        for row in reader:
            try:
                if not (len(row)):
                    continue
                if row[0] not in ["car", "truck", "spec_machine"]:
                    raise ValueError
                if row[1] == "":
                    raise ValueError
                if not len(os.path.splitext(row[3])[1]):
                    raise ValueError
                if row[0] == "car" and not row[2].isdigit():
                    raise ValueError
                if row[0] == "spec_machine" and row[6] == "":
                    raise ValueError
                if row[3] == "":
                    raise ValueError
                if not float(row[5]):
                    raise ValueError
            except ValueError:
                continue
            else:
                if row[0] == "car":
                    car_list.append(Car(row[1], row[3], row[5], row[2]))
                if row[0] == "truck":
                    car_list.append(Truck(row[1], row[3], row[5], row[4]))
                if row[0] == "spec_machine":
                    car_list.append(SpecMachine(row[1], row[3], row[5], row[6]))

    return car_list


