"""
    Class derived from Ilya Zhelyabuzhsky stockfish.py class(https://github.com/zhelyabuzhsky/stockfish)
    :copyright: (c) 2016 by Ilya Zhelyabuzhsky.
    :license: GPLv3
"""

import subprocess


class UCIP:
    """Outil permetant d'integrer un moteur d'échecs utilisant le UCIP (Universal Chess Interface Protocol)"""

    def __init__(self, command, depth=None, param=None):
        if param is None:
            param = {}
        self.ucip = subprocess.Popen(
            command,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        self.depth = str(depth)
        self.__put('uci')
        for name, value in list(param.items()):
            self.__set_option(name, value)

        self.__start_new_game()

    def __start_new_game(self):
        self.__put('ucinewgame')
        self.__isready()

    def __put(self, command):
        self.ucip.stdin.write(command + '\n')
        self.ucip.stdin.flush()

    def __set_option(self, optionname, value):
        self.__put('setoption name %s value %s' % (optionname, str(value)))
        stdout = self.__isready()
        if stdout.find('No such') >= 0:
            print('lczero was unable to set option %s' % optionname)

    def __isready(self):
        self.__put('isready')
        while True:
            text = self.ucip.stdout.readline().strip()
            if text == 'readyok':
                return text

    def __go(self):
        self.__put('go depth %s' % self.depth)

    @staticmethod
    def __convert_move_list_to_str(moves):
        result = ''
        for move in moves:
            result += move + ' '
        return result.strip()

    def set_position(self, moves=None):
        """Sets current board positions.

        Args:
            moves: A list of moves to set this position on the board.
                Must be in full algebraic notation.
                example:
                ['e2e4', 'e7e5']

        Returns:
            None
        """
        if moves is None:
            moves = []
        self.__put('position startpos moves %s' %
                   self.__convert_move_list_to_str(moves))

    def set_fen_position(self, fen_position):
        self.__put('position fen ' + fen_position)

    def get_best_move(self):
        """Get best move with current position on the board.

        Returns:
            A string of move in algebraic notation or False, if it's a mate now.
        """
        self.__go()
        while True:
            text = self.ucip.stdout.readline().strip()
            split_text = text.split(' ')
            if split_text[0] == 'bestmove':
                if split_text[1] == '(none)':
                    return False
                return split_text[1]

    def is_move_correct(self, move_value):
        """Checks new move.

        Args:
            move_value: New move value in algebraic notation.

        Returns:
            True, if new move is correct, else False.
        """
        self.__put('go depth 1 searchmoves %s' % move_value)
        while True:
            text = self.ucip.stdout.readline().strip()
            split_text = text.split(' ')
            if split_text[0] == 'bestmove':
                if split_text[1] == '(none)':
                    return False
                else:
                    return True

    def __del__(self):
        self.ucip.kill()
