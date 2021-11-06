###############################################################################
# FILE : board.py
# WRITER : Seggev Haimovich , seggev , 206729295
# EXERCISE : intro2cs2 ex9 2021
# DESCRIPTION: the class - board
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: none
# NOTES: none
###############################################################################

class Board:
    """
    A class for the board object.
    the class builds a board with nothing inside it, in the size of 7X7.
    the purpose of this class is to organize all the cars and their information
    in one place, each car don't "know" about the others and the board can
    "tell" the game all the information.
    """
    __SIZE = 7
    __GOAL = (3, 7)

    def __init__(self):
        self.__cars = []

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        for car in self.__cars:
            if coordinate in car.car_coordinates():
                return car.get_name()

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        coord_lst = []
        for i in range(Board.__SIZE):
            for j in range(Board.__SIZE):
                coord_lst.append((i, j))
        coord_lst.append(Board.__GOAL)
        return coord_lst

    def __legal_place(self, coordinate):
        """
        checks if the coordinate given is empty and in the board boundaries.
        this function is not part of the API, it helps the other function.
        :param coordinate: tuple of the coordinate we want to check
        :return: True if empty and exists, False otherwise
        """
        if self.cell_content(
                coordinate) is None and coordinate in self.cell_list():
            return True
        return False

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description)
                 representing legal moves
        """
        all_moves_poss = []
        for car in self.__cars:
            for direction in car.possible_moves():
                if self.__legal_place(car.movement_requirements(direction)[0]):
                    all_moves_poss.append((car.get_name(), direction,
                                           car.possible_moves()[direction]))
        return all_moves_poss

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be
        filled for victory.
        :return: (row,col) of goal location
        """
        return Board.__GOAL

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        for car_check in self.__cars:
            if car.get_name() == car_check.get_name():
                return False
        for coordinate in car.car_coordinates():
            if not self.__legal_place(coordinate):
                return False
        self.__cars.append(car)
        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        if not self.__cars:
            return False
        for car in self.__cars:
            if car.get_name() == name:
                break
        if self.__legal_place(car.movement_requirements(movekey)[0]):
            if car.move(movekey):
                return True
        return False

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        word = ''
        for i in range(Board.__SIZE):
            for j in range(Board.__SIZE):
                if self.cell_content((i, j)) is None:
                    word += '_ '
                else:
                    word += self.cell_content((i, j)) + ' '
                if i == 3 and j == 6:
                    if self.cell_content(self.target_location()) is None:
                        word += '*'
                    else:
                        word += self.cell_content(self.target_location())
            word += '\n'
        return word
