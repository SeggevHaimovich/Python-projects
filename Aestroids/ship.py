###############################################################################
# FILE : ship.py
# WRITER : ShirHadad Seggev Haimovich, seggev shirhdd
# EXERCISE : intro2cs2 ex10 2021
# DESCRIPTION: The class: Ship
###############################################################################
class Ship:
    """
    A class for the ship object.
    the class builds a ship object with the following information: location,
    speed, direction, radius and life.
    the ship object purpose is to save all the data of the ship.
    """
    INITIAL_LIFE = 3
    RADIUS = 1

    def __init__(self, location, speed, direction):
        """
        builds the ship object.
        get the location, speed and direction from the class call.
        sets the radius and the life to the initial values. (radius-1, life-3)
        :param location: tuple (x and y coordinates)
        :param speed: tuple (speed in x direction and y direction)
        :param direction: int (degrees)
        """
        self.__location = location
        self.__speed = speed
        self.__direction = direction
        self.__radius = Ship.RADIUS
        self.__life = Ship.INITIAL_LIFE

    def get_location(self):
        """
        :return: the current location of the ship
        """
        return self.__location

    def get_speed(self):
        """
        :return: the current speed of the ship
        """
        return self.__speed

    def get_radius(self):
        """
        :return: the radius of the ship
        """
        return self.__radius

    def get_direction(self):
        """
        :return: the current direction of the ship
        """
        return self.__direction

    def get_life(self):
        """
        :return: the current life of the ship
        """
        return self.__life

    def reduce_life(self):
        """
        reduces the life of the ship by 1.
        :return: None
        """
        self.__life -= 1

    def set_location(self, x, y):
        """
        changes the location of the ship to the given coordinates
        :param x: float
        :param y: float
        :return: None
        """
        self.__location = (x, y)

    def set_speed(self, x, y):
        """
        changes the speed of the ship to the given speed.
        :param x: float
        :param y: float
        :return: None
        """
        self.__speed = (x, y)

    def change_direction(self, degree):
        """
        changes the direction of the ship, adding the given degrees.
        :param degree: int
        :return: None
        """
        self.__direction += degree
