import random
import simulator_position as pos_gen


class User:

    AVG_HRATE = 75      # average heart rate
    VAR_HRATE = 15      # heart rate variance
    AVG_SPEED = 0.0005  # average speed [km/s]
    VAR_SPEED = 0.0001  # average speed [km/s]
    SAFETY_PROB = 0.7

    def __init__(self, sensor_id, name, email):
        # Generate user data
        self._sensor_id = sensor_id
        self._name = name
        self._email = email
        self._avg_hrate = int(random.gauss(User.AVG_HRATE, User.VAR_HRATE))
        self._var_hrate = User.VAR_HRATE
        self._safety_latitude = random.uniform(-90, 90)
        self._safety_longitude = random.uniform(-180, 180)
        self._current_latitude = self._safety_latitude
        self._current_longitude = self._safety_longitude
        self._safety_radius = random.uniform(0.5, 1)    # [km]
        self._avg_speed = random.gauss(User.AVG_SPEED, User.VAR_SPEED)

    def current_hrate(self):
        return int(random.gauss(self.avg_hrate, self.var_hrate))

    def next_position(self, period):
        max_distance = self.avg_speed * period
        distance = self.safety_radius if random.random() < User.SAFETY_PROB else max_distance
        latitude = self.safety_latitude
        longitude = self.safety_longitude
        seed = None  # current system time
        self.current_latitude, self.current_longitude = \
            pos_gen.get_random_position(latitude, longitude, seed, 0, distance)

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
    def current_latitude(self):
        return self._current_latitude

    @property
    def current_longitude(self):
        return self._current_longitude

    @property
    def email(self):
        return self._email

    @property
    def safety_radius(self):
        return self._safety_radius

    @property
    def avg_speed(self):
        return self._avg_speed

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @safety_latitude.setter
    def safety_latitude(self, new_lat):
        self._safety_latitude = new_lat

    @safety_longitude.setter
    def safety_longitude(self, new_long):
        self._safety_longitude = new_long

    @current_latitude.setter
    def current_latitude(self, new_lat):
        self._current_latitude = new_lat

    @current_longitude.setter
    def current_longitude(self, new_lat):
        self._current_longitude = new_lat


if __name__ == '__main__':
    user = User(1, "test", "nonnocare.notify@gmail.com")
    for i in range(10):
        user.next_position(120)
        print("Heart rate:", user.current_hrate())
        print("latitude:", user.current_latitude)
        print("longitude:", user.current_longitude)
