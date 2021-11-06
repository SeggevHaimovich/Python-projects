###############################################################################
# FILE : car.py
# WRITER : Seggev Haimovich , seggev , 206729295
# EXERCISE : intro2cs2 ex9 2021
# DESCRIPTION: the class - car
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: none
# NOTES: none
###############################################################################

class Car:
    """
    A class for the car object.
    the class builds a car object with the following information: name, length,
    location and orientation
    the name is a string.
    the length is an int represent the number of squares the car takes
    the location describe the head square of the car
    the orientation describe if the car is vertical or horizontal
    """
    __DIRECTIONS = {'UP': 'u', 'DOWN': 'd', 'RIGHT': 'r', 'LEFT': 'l'}
    __ORIENTATION = {'VERTICAL': 0, 'HORIZONTAL': 1}

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple represents the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.name = name
        self.length = length
        self.location = location
        self.orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        locations_lst = []
        if self.orientation == Car.__ORIENTATION['VERTICAL']:
            for i in range(self.length):
                locations_lst.append((self.location[0] + i, self.location[1]))
        elif self.orientation == Car.__ORIENTATION['HORIZONTAL']:
            for i in range(self.length):
                locations_lst.append((self.location[0], self.location[1] + i))
        return locations_lst

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements
        permitted by this car.
        """
        if self.orientation == Car.__ORIENTATION['VERTICAL']:
            return {'u': "move the car up", 'd': "move the car down"}
        elif self.orientation == Car.__ORIENTATION['HORIZONTAL']:
            return {'r': "move the car right", 'l': "move the car left"}
        return {}

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this
        move to be legal.
        """
        if self.orientation == Car.__ORIENTATION['VERTICAL']:
            if movekey == Car.__DIRECTIONS['UP']:
                return [(self.location[0] - 1, self.location[1])]
            if movekey == Car.__DIRECTIONS['DOWN']:
                return [(self.location[0] + self.length, self.location[1])]
        if self.orientation == Car.__ORIENTATION['HORIZONTAL']:
            if movekey == Car.__DIRECTIONS['RIGHT']:
                return [(self.location[0], self.location[1] + self.length)]
            if movekey == Car.__DIRECTIONS['LEFT']:
                return [(self.location[0], self.location[1] - 1)]
        return []

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if movekey not in self.possible_moves():
            return False
        location_lst = list(self.location)
        if self.orientation == Car.__ORIENTATION['VERTICAL']:
            if movekey == Car.__DIRECTIONS['DOWN']:
                location_lst[0] += 1
                self.location = tuple(location_lst)
            else:
                location_lst[0] -= 1
                self.location = tuple(location_lst)
        else:
            if movekey == Car.__DIRECTIONS['RIGHT']:
                location_lst[1] += 1
                self.location = tuple(location_lst)
            else:
                location_lst[1] -= 1
                self.location = tuple(location_lst)
        return True

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.name
