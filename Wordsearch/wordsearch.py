###############################################################################
# FILE : wordsearch.py
# WRITER : Seggev Haimovich , seggev , 206729295
# EXERCISE : intro2cs2 ex5 2021
# DESCRIPTION: searches words in matrix in the directions the user wants
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: none
# NOTES: none
###############################################################################
import sys
from copy import deepcopy
import os

RIGHT = 'r'
LEFT = 'l'
UP = 'u'
DOWN = 'd'
UP_RIGHT = 'w'
UP_LEFT = 'x'
DOWN_RIGHT = 'y'
DOWN_LEFT = 'z'
GOOD_DIRECTIONS = ['r', 'l', 'u', 'd', 'w', 'x', 'y', 'z']


def read_wordlist(filename):
    """
    gets the name of the words list's file and return list of the words in
    the file
    :param filename: string
    :return: word list (list)
    """
    with open(filename, 'r') as f:
        word_lst = f.read().split()
    return word_lst


def read_matrix(filename):
    """
    gets the name of matrix's file and return list of lists that represents
    the matrix
    :param filename: string
    :return: matrix (list)
    """
    with open(filename, 'r') as f:
        matrix = []
        for line in f:
            matrix.append(list(line.split(',')))
            matrix[-1][-1] = list(matrix[-1][-1])[0]
    return matrix


def check_and_read_parameters(lst):
    """
    checks if the parameters given are ok.
    prints a message to the user if not.
    reads the words list and the matrix into lists.
    return the values of the word-file (as a list of words), matrix-file (as a
    matrix), output-file and directions.
    if the input isn't good returns 0 for all the values.
    :param lst: list
    :return: word_list (list), matrix (list), output_file (string),
    directions (string)
    """
    if len(lst) != 4:
        print("You didn't enter 4 parameters")
        return 0, 0, 0, 0
    word_file, matrix_file, output_file, directions = lst
    if not os.path.isfile(word_file):
        print("The words file does not exist")
        return 0, 0, 0, 0
    word_list = read_wordlist(word_file)
    if not os.path.isfile(matrix_file):
        print('The matrix file does not exist')
        return 0, 0, 0, 0
    matrix = read_matrix(matrix_file)
    for letter in directions:
        if letter not in GOOD_DIRECTIONS:
            print('You entered a wrong direction')
            return 0, 0, 0, 0
    return word_list, matrix, output_file, directions


def set_up_dictionary(word_list):
    """
    setting up a dictionary. the keys are the words in the word list and the
    items are the number of times we found them in the matrix.
    :param word_list: list
    :return: dictionary (dict)
    """
    dictionary = dict()
    for word in word_list:
        dictionary[word] = 0
    return dictionary


def transpose_matrix(matrix):
    """
    transpose a matrix
    :param matrix: list
    :return: matrix (list)
    """
    transpose = []
    for col in range(len(matrix[0])):
        transpose.append([])
        for row in range(len(matrix)):
            transpose[-1].append(matrix[row][col])
    return transpose


def reverse_columns(matrix):
    """
    reverse the columns in a given matrix without changing the original matrix
    :param matrix: list
    :return: matrix (list)
    """
    new_matrix = deepcopy(matrix)
    for row in new_matrix:
        row[:] = row[::-1]
    return new_matrix


def reverse_rows(matrix):
    """
    reverse the rows in a given matrix without changing the original matrix
    :param matrix: list
    :return: matrix (list)
    """
    new_matrix = deepcopy(matrix)
    new_matrix[:] = new_matrix[::-1]
    return new_matrix


def search_right(word_list, matrix, dictionary):
    """
    searches words in the matrix in the direction: right
    update the values in the dictionary accordingly.
    :param word_list: list
    :param matrix: list
    :param dictionary: dict
    :return: dictionary (dict)
    """
    for word in word_list:
        for row in range(len(matrix)):
            for letter in range(len(matrix[row]) - len(word) + 1):
                if list(word) == matrix[row][letter:letter+len(word)]:
                    dictionary[word] += 1
    return dictionary


def search_left(word_list, matrix, dictionary):
    """
    searches words in the matrix in the direction: left
    update the values in the dictionary accordingly.
    :param word_list: list
    :param matrix: list
    :param dictionary: dict
    :return: dictionary (dict)
    """
    new_matrix = reverse_columns(matrix)
    dictionary = search_right(word_list, new_matrix, dictionary)
    return dictionary


def search_up(word_list, matrix, dictionary):
    """
    searches words in the matrix in the direction: up
    update the values in the dictionary accordingly.
    :param word_list: list
    :param matrix: list
    :param dictionary: dict
    :return: dictionary (dict)
    """
    transposed = transpose_matrix(matrix)
    dictionary = search_left(word_list, transposed, dictionary)
    return dictionary


def search_down(word_list, matrix, dictionary):
    """
    searches words in the matrix in the direction: down
    update the values in the dictionary accordingly.
    :param word_list: list
    :param matrix: list
    :param dictionary: dict
    :return: dictionary (dict)
    """
    new_matrix = transpose_matrix(matrix)
    dictionary = search_right(word_list, new_matrix, dictionary)
    return dictionary


def search_down_right(word_list, matrix, dictionary):
    """
    searches words in the matrix in the direction: diagonally down-right
    update the values in the dictionary accordingly.
    :param word_list: list
    :param matrix: list
    :param dictionary: dict
    :return: dictionary (dict)
    """
    for word in word_list:
        lst_word = list(word)
        for row in range(len(matrix) - len(word) + 1):
            for letter in range(len(matrix[0]) - len(word) + 1):
                is_it_right = True
                for i in range(len(word)):
                    if lst_word[i] != matrix[row+i][letter+i]:
                        is_it_right = False
                        break
                if is_it_right:
                    dictionary[word] += 1
    return dictionary


def search_down_left(word_list, matrix, dictionary):
    """
    searches words in the matrix in the direction: diagonally down-left
    update the values in the dictionary accordingly.
    :param word_list: list
    :param matrix: list
    :param dictionary: dict
    :return: dictionary (dict)
    """
    new_matrix = reverse_columns(matrix)
    dictionary = search_down_right(word_list, new_matrix, dictionary)
    return dictionary


def search_up_right(word_list, matrix, dictionary):
    """
    searches words in the matrix in the direction: diagonally up-right
    update the values in the dictionary accordingly.
    :param word_list: list
    :param matrix: list
    :param dictionary: dict
    :return: dictionary (dict)
    """
    new_matrix = reverse_rows(matrix)
    dictionary = search_down_right(word_list, new_matrix, dictionary)
    return dictionary


def search_up_left(word_list, matrix, dictionary):
    """
    searches words in the matrix in the direction: diagonally up-left
    update the values in the dictionary accordingly.
    :param word_list: list
    :param matrix: list
    :param dictionary: dict
    :return: dictionary (dict)
    """
    new_matrix = reverse_rows(matrix)
    dictionary = search_down_left(word_list, new_matrix, dictionary)
    return dictionary


def make_list(dictionary):
    """
    making a list of tuples, each tuple contain a key and it's item.
    contain only the items with value other then 0
    :param dictionary: dict
    :return: list of tuples (list)
    """
    lst = []
    for key in dictionary:
        if dictionary[key]:
            lst.append((key, dictionary[key]))
    return lst


def find_words(word_list, matrix, directions):
    """
    gets the list of the words to check, the matrix to check in and the
    directions to check and checks how many times every words exists in
    those terms.
    returns a list with tuples, each tuple contains the word and the amount
    of times this word appears in those terms.
    :param word_list: list
    :param matrix: list
    :param directions: string
    :return: results (list)
    """
    dictionary = set_up_dictionary(word_list)
    if word_list == [] or matrix == []:
        return []
    if RIGHT in directions:
        dictionary = search_right(word_list, matrix, dictionary)
    if LEFT in directions:
        dictionary = search_left(word_list, matrix, dictionary)
    if UP in directions:
        dictionary = search_up(word_list, matrix, dictionary)
    if DOWN in directions:
        dictionary = search_down(word_list, matrix, dictionary)
    if UP_RIGHT in directions:
        dictionary = search_up_right(word_list, matrix, dictionary)
    if UP_LEFT in directions:
        dictionary = search_up_left(word_list, matrix, dictionary)
    if DOWN_RIGHT in directions:
        dictionary = search_down_right(word_list, matrix, dictionary)
    if DOWN_LEFT in directions:
        dictionary = search_down_left(word_list, matrix, dictionary)
    results = make_list(dictionary)
    return results


def write_output(results, filename):
    """
    writes the results in a given name file.
    :param results: list
    :param filename: string
    :return: None
    """
    with open(filename, 'w') as f:
        for i in results:
            f.write(i[0] + ',' + str(i[1]) + '\n')


def main():
    """
    find how many times a word from a word-list appears in a given matrix
    and writes it in a file.
    :return: None
    """
    input_lst = sys.argv[1:]
    word_list, matrix, output_file, directions = check_and_read_parameters(
        input_lst)
    if word_list != 0:
        write_output(find_words(word_list, matrix, directions), output_file)


if __name__ == '__main__':
    main()
