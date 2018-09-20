import curses
from itertools import chain

from grid import Action, Grid
from screen import Screen

######################################
# 1. 初始游戏                         #
# 2. 游戏过程                         #
# 3. 游戏失败                         #
# 4. 游戏成功                         #
# 5. 退出游戏                         #
# 6. 重置游戏                         #
######################################


class Game:
    def __init__(self, size=4, win_num=2048):
        self.size = size
        self.win_num = win_num
        self.state = 'init'
        self.win = False
        self.over = False
        self.score = 0
        self.grid = Grid(self.size, self.score)
        self.reset()

    def reset(self):
        self.state = 'init'
        self.win = False
        self.over = False
        self.score = 0
        self.grid = Grid(self.size, self.score)
        self.grid.reset()

    @property
    def screen(self):
        return Screen(screen=self.command, score=self.score, grid=self.grid)

    def move(self, direction):
        if self.can_move(direction):
            getattr(self.grid, 'move_' + direction)()
            self.grid.add_random_item()
            return True
        else:
            return False

    @property
    def is_win(self):
        self.win = max(chain(*self.grid.cells)) >= self.win_num
        return self.win

    @property
    def is_lose(self):
        self.over = not any(
            self.can_move(move) for move in self.action.actions)
        return self.over

    def can_move(self, direction):
        return getattr(self.grid, 'can_move_' + direction)()

    def state_init(self):
        self.reset()
        return 'game'

    def state_game(self):
        self.screen.draw()
        action = self.action.get_player_action()

        if action == Action.RESTART:
            return 'init'
        if action == Action.EXIT:
            return 'exit'
        if self.move(action):
            if self.is_win:
                return 'win'
            if self.is_lose:
                return 'over'
        return 'game'

    def _restart_or_exit(self):
        self.screen.draw()
        return 'init' if self.action.get_player_action(
        ) == Action.RESTART else 'exit'

    def state_win(self):
        return self._restart_or_exit()

    def state_over(self):
        return self._restart_or_exit()

    def __call__(self, command):
        curses.use_default_colors()
        self.command = command
        self.action = Action(command)
        while self.state != 'exit':
            self.state = getattr(self, 'state_' + self.state)()
