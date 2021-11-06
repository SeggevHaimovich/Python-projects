###############################################################################
# FILE : torpedo.py
# WRITER : ShirHadad Seggev Haimovich, seggev shirhdd
# EXERCISE : intro2cs2 ex10 2021
# DESCRIPTION: the class GameRunner and the main function.
###############################################################################


from screen import Screen
import random
import ship
import asteroid
import torpedo
import math
import sys

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:
    """
    A class for the GameRunner object.
    this class runs the game "ASTEROIDS", using the classes 'Ship', 'Asteroid',
    'Torpedo' and 'Screen'.
    it does loops of checks for inputs from the player, when it gets input it
    react accordingly.
    it has many variables, most of the are permanent.
    it ends the game when the player lose, win or quit.
    """
    SCORE_SIZE_DICT = {3: 20, 2: 50, 1: 100}
    POSSIBLE_SPEED = [4, 3, 2, 1, -1, -2, -3, -4]
    EXPLOSION_MESSAGE = ("!@!@!@@!", "Be careful from asteroids")
    QUIT_MESSAGE = {
        "win": ("YOU WON!!!", "you are the best we have ever seen"),
        "lose": ("YOU LOST", "Go take some private lessons"),
        "quit": ("quitter", "don't goooooooooooooooooooooooooooo")}
    TORPEDOES_MAX_AMOUNT = 10

    def __init__(self, asteroids_amount=DEFAULT_ASTEROIDS_NUM):
        """
        builds the gamerunner object.
        creates the screen and sets it's size to the default size.
        create the ship of the game with random place, without speed and
        direction 0.
        sets the asteroids amount to the default unless it gets number from the
        class call.
        creates asteroids and torpedoes list to save them all.
        sets the score to the initial score (0).
        and calling the function start game.
        :param asteroids_amount:
        """
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__ship = ship.Ship((random.randint(self.__screen_min_x,
                                                self.__screen_max_x),
                                 random.randint(self.__screen_min_y,
                                                self.__screen_max_y)), (0, 0),
                                0)
        self.__asteroids_amount = asteroids_amount
        self.__asteroids_list = []
        self.__torpedoes_list = []
        self.__score = 0
        self.start_game()

    def start_game(self):
        """
        This function draws the first ship on the screen and the asteroids.
        :return: None
        """
        self.__screen.draw_ship(self.__ship.get_location()[0],
                                self.__ship.get_location()[1],
                                self.__ship.get_direction())
        self.build_asteroids()

    def build_asteroids(self):
        """
        The function chooses a random position to the asteroids and draws them
        :return: None
        """
        for i in range(self.__asteroids_amount):
            while True:
                random_x = random.randint(self.__screen_min_x,
                                          self.__screen_max_x)
                random_y = random.randint(self.__screen_min_y,
                                          self.__screen_max_y)
                if random_y != self.__ship.get_location()[1] or random_x != \
                        self.__ship.get_location()[0]:
                    break
            astr = asteroid.Asteroid((random_x, random_y), (
                     random.choice(GameRunner.POSSIBLE_SPEED),
                     random.choice(GameRunner.POSSIBLE_SPEED)))
            self.__asteroids_list.append(astr)
            self.__screen.register_asteroid(astr, astr.INITIAL_SIZE_ASTEROID)
            self.__screen.draw_asteroid(astr, random_x, random_y)

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        The function runs our loops for each object in our game.
        :return: None
        """
        self.__asteroid_loop()
        self.__ship_loop()
        self.__torpedo_loop()
        if self.__end_loop():
            self.__screen.end_game()
            sys.exit()

    def __ship_loop(self):
        """
        The function draws the ship and updates it's spot if a button is
        clicked and sets the ships new location.
        :return: None
        """
        self.__screen.draw_ship(self.__ship.get_location()[0],
                                self.__ship.get_location()[1],
                                self.__ship.get_direction())
        self.ship_is_pressed()
        self.__ship.set_location(*self.__new_spot(self.__ship.get_location(),
                                                  self.__ship.get_speed()))

    def ship_is_pressed(self):
        """
        The function checks if something is pressed and activates the concrete
        action on the ship.
        :return: None
        """
        if self.__screen.is_right_pressed():
            self.__ship.change_direction(-7)
        if self.__screen.is_left_pressed():
            self.__ship.change_direction(7)
        if self.__screen.is_up_pressed():
            self.__new_speed(self.__ship.get_speed(),
                             math.radians(self.__ship.get_direction()))

    def __asteroid_loop(self):
        """
        The function creates the asteroids and keeps on drawing the new spots
        when they move on to the screen.
        :return: None
        """
        for astr in self.__asteroids_list:
            n_spot_x, n_spot_y = self.__new_spot(astr.get_location(),
                                                 astr.get_speed())
            astr.set_location(n_spot_x, n_spot_y)
            self.__screen.draw_asteroid(astr, n_spot_x, n_spot_y)
            if astr.has_intersection(self.__ship):
                self.__crash(astr)
                continue
            for tor in self.__torpedoes_list:
                if astr.has_intersection(tor):
                    self.__explode(astr, tor)
                    break

    def __crash(self, astr):
        """
        update the life of the ship, removes the asteroid and prints message
        when there is a crush between the ship and an asteroid.
        :param astr: asteroid
        :return: None
        """
        self.__ship.reduce_life()
        self.__screen.show_message(GameRunner.EXPLOSION_MESSAGE[0],
                                   GameRunner.EXPLOSION_MESSAGE[1])
        self.__screen.remove_life()
        self.__asteroids_list.remove(astr)
        self.__screen.unregister_asteroid(astr)

    def __torpedo_loop(self):
        """
        The function generates new spots to the torpedos each time. Every
        loop the function checks if there was an intersection between an
        asteroid and updates the screen according to that by splitting the
        asteroids if their big or deleting them from the screen if they are
        the smallest size.
        :return: None
        """
        self.__create_torpedoes()
        for tor in self.__torpedoes_list:
            n_spot_x, n_spot_y = self.__new_spot(tor.get_location(),
                                                 tor.get_speed())
            tor.set_location(n_spot_x, n_spot_y)
            self.__screen.draw_torpedo(tor, n_spot_x, n_spot_y,
                                       tor.get_direction())
            tor.reduce_lifetime()
            if tor.dead_torpedo():
                self.__torpedoes_list.remove(tor)
                self.__screen.unregister_torpedo(tor)

    def __create_torpedoes(self):
        """
        The function creates the torpedoes and adds them to the list of
        torpedoes while calculating the speed and spot for each one.
        :return: None
        """
        if self.__screen.is_space_pressed() and len(
                self.__torpedoes_list) < GameRunner.TORPEDOES_MAX_AMOUNT:
            speed_x = self.__ship.get_speed()[0] + 2 * math.cos(
                math.radians(self.__ship.get_direction()))
            speed_y = self.__ship.get_speed()[1] + 2 * math.sin(
                math.radians(self.__ship.get_direction()))
            torp = torpedo.Torpedo(self.__ship.get_location(),
                                   (speed_x, speed_y),
                                   self.__ship.get_direction())
            self.__torpedoes_list.append(torp)
            self.__screen.register_torpedo(torp)

    def __explode(self, astr, torp):
        """
        The function updates the score, list of torpedoes and asteroids when
        there is an explosion between a torpedo and a asteroid.
        :param astr: asteroid object
        :param torp: torpedo object
        :return: None
        """
        self.__score += GameRunner.SCORE_SIZE_DICT[astr.get_size()]
        self.__screen.set_score(self.__score)
        self.__asteroids_list.remove(astr)
        self.__screen.unregister_asteroid(astr)
        self.__torpedoes_list.remove(torp)
        self.__screen.unregister_torpedo(torp)
        if astr.get_size() != 1:
            self.__split_asteroid(astr, torp)

    def __split_asteroid(self, astr, torp):
        """
        The function deals with the splitting of the asteroid when they are
        getting shot by a torpedo. It creates two new asteroids with smaller
        sizes and removed the old exploded asteroid.
        :param astr: asteroid object
        :param torp: torpedo object
        :return: None
        """
        new_size = int(math.ceil(astr.get_size() / 2))
        distance = math.sqrt(
            astr.get_speed()[0] ** 2 + astr.get_speed()[1] ** 2)
        new_astroid_speed_x = (torp.get_speed()[0] + astr.get_speed()[
            0]) / distance
        new_astroid_speed_y = (torp.get_speed()[1] + astr.get_speed()[
            1]) / distance
        astr1 = asteroid.Asteroid(astr.get_location(),
                                  (new_astroid_speed_x, new_astroid_speed_y),
                                  new_size)
        astr2 = asteroid.Asteroid(astr.get_location(),
                                  (-new_astroid_speed_x,
                                   -new_astroid_speed_y), new_size)
        self.__asteroids_list += [astr1, astr2]
        self.__screen.register_asteroid(astr1, new_size)
        self.__screen.register_asteroid(astr2, new_size)

    def __new_spot(self, old_spot, speed):
        """
        The function calculates the new spot according to the speed and old
        spot it received.
        :param old_spot: tuple
        :param speed: tuple
        :return: tuple (x, y)
        """
        delta_x = self.__screen_max_x - self.__screen_min_x
        delta_y = self.__screen_max_y - self.__screen_min_y
        new_spot_x = self.__screen_min_x + (
                    old_spot[0] + speed[0] - self.__screen_min_x) % delta_x
        new_spot_y = self.__screen_min_y + (
                    old_spot[1] + speed[1] - self.__screen_min_y) % delta_y
        return new_spot_x, new_spot_y

    def __new_speed(self, old_speed, heading):
        """
        The function calculates the new speed and updates the ship.
        :param old_speed: tuple
        :param heading: int
        :return: None
        """
        new_speed_x = old_speed[0] + math.cos(heading)
        new_speed_y = old_speed[1] + math.sin(heading)
        self.__ship.set_speed(new_speed_x, new_speed_y)
        return new_speed_x, new_speed_y

    def __end_loop(self):
        """
        The function checks if the game should end for one of the following
        reasons: no life left, if there are no more asteroids in the game
        or if the player has clicked to exit game. We show a message to the
        player for each option.
        :return: None
        """
        if self.__ship.get_life() == 0:
            self.__screen.show_message(GameRunner.QUIT_MESSAGE["lose"][0],
                                       GameRunner.QUIT_MESSAGE["lose"][1])
            return True
        if len(self.__asteroids_list) == 0:
            self.__screen.show_message(GameRunner.QUIT_MESSAGE["win"][0],
                                       GameRunner.QUIT_MESSAGE["win"][1])
            return True
        if self.__screen.should_end():
            self.__screen.show_message(GameRunner.QUIT_MESSAGE["quit"][0],
                                       GameRunner.QUIT_MESSAGE["quit"][1])
            return True
        return False


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
