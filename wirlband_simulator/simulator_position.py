from random import seed
from random import gauss, random
from math import cos, sin, asin, atan2, degrees, radians


# da posizione in gradi decimali a gradi, primi, sec (41.85577° = 41 ° 51 ' 20 ")
def convert_dec_to_grad(grad):
    d = int(grad)
    m = int((grad - d) * 60)
    s = int((grad - d - m / 60) * 3600)

    return d, m, s


# da posizione in gradi primi secondi a decimali (41 ° 51 ' 20" = 41.85555)
def convert_grad_to_dec(d, m, s):
    rad = d + (m / 60) + (s / 3600)
    return rad


# da posizione in decimali a posizione in radianti (41.85555 = 0.73051725)
def convert_dec_to_rad(decimal):
    return radians(decimal)


# da posizione in radianti a posizione in decimali (0.73051725 = 41.85555)
def convert_rad_to_dec(rad):
    return degrees(rad)


# da una posizione in radianti ad un altra
def new_position_rad(lat, long, theta, d):
    # fi = latitudine
    # lambda = longitudine
    # theta = angolo (azimuth)
    # R = raggio della terra
    # d = distanza
    # delta= distanza angolare (d/R)
    # reference: http://www.movable-type.co.uk/scripts/latlong.html

    R = 6371

    new_lat = asin(sin(lat) * cos(d / R) +
                   cos(lat) * sin(d / R) * cos(theta))

    new_long = long + atan2(sin(theta) * sin(d / R) * cos(lat),
                            cos(d / R) - sin(lat) * sin(new_lat))

    return new_lat, new_long

# via del politecnico
#    old_lat = 41.85561
#    old_long = 12.62095


def get_random_position(lat, long, my_seed, min_d, max_d):
    # genera angolo random tra 0 e 360 gradi
    # seed random number generator
    seed(my_seed)

    # generate some Gaussian values
    theta = 360 * gauss(0, 1)
    if theta < 0:
        theta = 360 + theta

    # genera raggio random
    random_d = random()
    r = min_d + (random_d * (max_d - min_d))

    lat = convert_dec_to_rad(lat)
    long = convert_dec_to_rad(long)
    theta = convert_dec_to_rad(theta)

    new_lat_rad, new_long_rad = new_position_rad(lat, long, theta, r)

    new_lat = convert_rad_to_dec(new_lat_rad)
    new_long = convert_rad_to_dec(new_long_rad)

    return new_lat, new_long


def main():

    # get position: https://stevemorse.org/jcal/latlon.php
    print(get_random_position(41.85561, 12.62095, 123, 0, 0.5))


if __name__ == '__main__':
    main()
