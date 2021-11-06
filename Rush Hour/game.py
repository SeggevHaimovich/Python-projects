###############################################################################
# FILE : game.py
# WRITER : Seggev Haimovich , seggev , 206729295
# EXERCISE : intro2cs2 ex9 2021
# DESCRIPTION: the class game and the main function
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: none
# NOTES: none
###############################################################################

import sys
from car import *
from board import *
import helper

NAMES = ['Y', 'B', 'O', 'W', 'G', 'R']
ORIENTATION = {'VERTICAL': 0, 'HORIZONTAL': 1}
VALID_LENGTH = {'MINIMUM': 2, 'MAXIMUM': 4}


class Game:
    """
    A class for the object game.
    the object built with a board object related to it.
    the game object runs has the rules and the play method in it, using the
    board information it runs the game "RUSH-HOUR"
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.board = board

    def __get_user_input(self):
        """
        getting the user input for the next move.
        this function is not part of the API, it helps the other function.
        :return:tuple - name of the car and direction to move. if the user want
        to exit the game and enters '!' returns 0,0
        """
        while True:
            inp = input(
                "please enter the name of the car you want to move and the "
                "direction you want to move it.")
            if inp == '!':
                return 0, 0
            if len(inp) != 3:
                print('you entered invalid input, it should look like: Y,d')
                continue
            name, comma, direction = inp
            if comma != ',':
                print('you entered invalid input, it should look like: Y,d')
                continue
            for move in self.board.possible_moves():
                if name == move[0] and direction == move[1]:
                    return name, direction
            print(
                'you enter invalid input, the name of the car or the direction'
                ' you gave were wrong')

    def __single_turn(self):
        """
        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.
        """
        while True:
            name, direction = self.__get_user_input()
            if name == 0:  # if the user's input was '!'
                return 0
            if not self.board.move_car(name, direction):
                print("the move you want to do can't be done")
                continue
            break

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        print('Welcome to "RUSH-HOUR"\n'
              'to move the cars you need to type the name of the car and the '
              'direction you want it to move.\n'
              'you need to press one of the following to pick the direction:\n'
              'u - to move up, d - to move down, l - to move left, r - to move'
              ' right)')
        while True:
            print(self.board)
            if self.board.cell_content(self.board.target_location()):
                print('CONGRATULATIONS!!\n'
                      'you won the game')
                break
            if self.__single_turn() == 0:  # if the user's input was '!'
                print("sorry to see you go, Bye Bye")
                break


def check_data(name, length, location, orientation):
    """
    checks the data of the car given.
    :param name: the name of the car (string)
    :param length: the length of the car (int)
    :param location: the location of the car (list)
    :param orientation: the orientation of the car (int)
    :return: True if the car has valid parameters, False otherwise
    """
    if not (isinstance(name, str) and isinstance(length, int) and isinstance(
            location, list) and isinstance(orientation, int)):
        return False
    if len(location) != 2 or not isinstance(location[0],
                                            int) or not isinstance(location[1],
                                                                   int):
        return False
    if name not in NAMES:
        return False
    if not VALID_LENGTH['MINIMUM'] <= length <= VALID_LENGTH['MAXIMUM']:
        return False
    if orientation not in ORIENTATION.values():
        return False
    return True


def add_cars_to_board(board, car_config):
    """
    adds all the cars given in the json file to the board given.
    :param board: board object
    :param car_config: dictionary with all the cars names and their parameters
    :return:None
    """
    for name in car_config:
        length, location, orientation = car_config[name]
        if not check_data(name, length, location, orientation):
            continue
        board.add_car(Car(name, length, tuple(location), orientation))


if __name__ == "__main__":
    car_config = helper.load_json(sys.argv[1])
    board = Board()
    add_cars_to_board(board, car_config)
    game = Game(board)
    game.play()
