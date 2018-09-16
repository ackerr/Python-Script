class Screen:
    """ 用来生成布局 """
    move_string = '(W)Up (S)Down (A)Left (D)Right'
    help_string = '      (R)Restart (Q)Exit'
    lose_string = '        GAME OVER'
    win_string = '         YOU WIN'

    def __init__(self, screen=None, score=0, best_score=0, is_win=False, is_lose=False, grid=None):
        self.screen = screen
        self.score = score
        self.best_score = best_score
        self.is_win = is_win
        self.is_lose = is_lose
        self.grid = grid
        self.counter = 0

    def cast(self, string):
        self.screen.addstr(string + '\n')

    def draw_row(self, row):
        self.cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

    def draw(self):
        self.screen.clear()
        # self.cast('SCORE: ' + str(self.score))
        if self.best_score != 0:
            self.cast('BEST_SCORE: ' + str(self.best_score))

        for row in self.grid.cells:
            self.cast('+' + ('-------' * self.grid.size + '+'))
            self.draw_row(row)
        self.cast('+' + ('-------' * self.grid.size + '+'))

        if self.is_win:
            self.cast(self.win_string)
        else:
            if self.is_lose:
                self.cast(self.lose_string)
            else:
                self.cast(self.move_string)
        self.cast(self.help_string)
