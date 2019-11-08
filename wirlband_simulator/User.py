import random


class User:

    AVG_HRATE = 75
    VAR_HRATE = 15

    def __init__(self, sensor_id, name, email):
        # Generate user data
        self._sensor_id = sensor_id
        self._name = name
        self._avg_hrate = int(random.gauss(User.AVG_HRATE, User.VAR_HRATE))
        self._var_hrate = User.VAR_HRATE
        self._safety_latitude = random.uniform(-90, 90)
        self._safety_longitude = random.uniform(-180, 180)
        # safety_radius = random.uniform(10, 15)
        self._email = email

    def current_hrate(self):
        return int(random.gauss(self.avg_hrate, self.var_hrate))

    def current_position(self):
        pass

    @property
    def name(self):
        return self._name

    @property
    def sensor_id(self):
        return self._sensor_id

    @property
    def avg_hrate(self):
        return self._avg_hrate

    @property
    def var_hrate(self):
        return self._var_hrate

    @property
    def safety_latitude(self):
        return self._safety_latitude

    @property
    def safety_longitude(self):
        return self._safety_longitude

    @property
    def email(self):
        return self._email

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @safety_latitude.setter
    def safety_latitude(self, new_lat):
        self._safety_latitude = new_lat

    @safety_longitude.setter
    def safety_longitude(self, new_long):
        self._safety_longitude = new_long


if __name__ == '__main__':
    user = User(1, "PUMA", "smvfal@gmail.com")
    print(user.current_hrate())