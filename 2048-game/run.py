import curses

from game import Game

if __name__ == '__main__':
    curses.wrapper(Game())
