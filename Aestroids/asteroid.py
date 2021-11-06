###############################################################################
# FILE : asteroid.py
# WRITER : ShirHadad Seggev Haimovich, seggev shirhdd
# EXERCISE : intro2cs2 ex10 2021
# DESCRIPTION: the class: Asteroid
###############################################################################

import math


class Asteroid:
    """
    A class for the asteroid object.
    the class builds an asteroid object with the following information:
    location, speed, size and radius.
    the asteroid object purpose is to save all the data of a single asteroid.
    """
    INITIAL_SIZE_ASTEROID = 3

    def __init__(self, location, speed, size=INITIAL_SIZE_ASTEROID):
        """
        builds the asteroid object.
        gets the location and speed from the class call.
        sets the size variable as the initial value unless it gets size from
        the class call.
        calculates the radius variable according to the size.
        :param location: tuple (x and y coordinates)
        :param speed: tuple (speed in x direction and y direction)
        :param size: int
        """
        self.__location = location
        self.__speed = speed
        self.__size = size
        self.__radius = self.__size * 10 - 5

    def get_location(self):
        """
        :return: the current location of the asteroid
        """
        return self.__location

    def get_speed(self):
        """
        :return: the current speed of the asteroid
        """
        return self.__speed

    def get_size(self):
        """
        :return: the size of the asteroid
        """
        return self.__size

    def get_radius(self):
        """
        :return: the radius of the asteroid
        """
        return self.__radius

    def set_location(self, x, y):
        """
        changes the location of the asteroid to the given coordinates.
        :param x: float
        :param y: float
        :return: None
        """
        self.__location = (x, y)

    def has_intersection(self, obj):
        """
        checks if the asteroid and the given object clash.
        :param obj: ship or torpedo
        :return:True if they clash and False otherwise
        """
        distance = math.sqrt(
            (obj.get_location()[0] - self.__location[0]) ** 2 + (
                        obj.get_location()[1] - self.__location[1]) ** 2)
        if distance <= (self.get_radius() + obj.get_radius()):
            return True
        return False
