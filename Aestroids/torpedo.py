###############################################################################
# FILE : torpedo.py
# WRITER : ShirHadad Seggev Haimovich, seggev shirhdd
# EXERCISE : intro2cs2 ex10 2021
# DESCRIPTION: the class Torpedo
###############################################################################

class Torpedo:
    """
    A class for the torpedo object.
    the class builds a torpedo object with the following information: location,
    speed, direction, radius and life.
    the torpedo object purpose is to save all the data of a single torpedo.
    """
    RADIUS = 4
    LIFE_TIME = 200

    def __init__(self, location, speed, direction):
        """
        builds the torpedo object.
        gets the location, speed and the direction from the class call.
        sets the radius and the lifetime to the initial values.
        :param location: tuple (x and y coordinates)
        :param speed: tuple (speed in x direction and y direction)
        :param direction: int (degrees)
        """
        self.__location = location
        self.__speed = speed
        self.__direction = direction
        self.__radius = Torpedo.RADIUS
        self.__lifetime = Torpedo.LIFE_TIME

    def get_location(self):
        """
        :return: the location of the torpedo.
        """
        return self.__location

    def get_radius(self):
        """
        :return: the radius of the torpedo.
        """
        return self.__radius

    def get_speed(self):
        """
        :return: the speed of the torpedo.
        """
        return self.__speed

    def get_direction(self):
        """
        :return: the direction of the torpedo.
        """
        return self.__direction

    def set_location(self, x, y):
        """
        sets the location of the torpedo to the given coordinates
        :param x: float
        :param y: float
        :return: None
        """
        self.__location = (x, y)

    def reduce_lifetime(self):
        """
        reduces the lifetime of the torpedo by 1.
        :return: None
        """
        self.__lifetime -= 1

    def dead_torpedo(self):
        """
        checks if the lifetime of the torpedo is over.
        :return: True if it's over and False otherwise
        """
        if self.__lifetime == 0:
            return True
        return False
