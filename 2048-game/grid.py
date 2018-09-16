from random import choice, randrange


class Action:
    UP = 'up'
    LEFT = 'left'
    DOWN = 'down'
    RIGHT = 'right'
    RESTART = 'restart'
    EXIT = 'exit'

    actions = [UP, LEFT, DOWN, RIGHT, RESTART, EXIT]  # 按键
    action_codes = [ord(code) for code in 'wasdrqWASDRQ']  # 按键的acsii值
    actions_dict = dict(zip(action_codes, actions * 2))  # 按键对应的命令

    def __init__(self, command):
        self.command = command

    def get_player_action(self):
        """ 获取用户的输入 """
        code = ''
        while code not in self.actions_dict:
            code = self.command.getch()
        return self.actions_dict[code]


class Grid:
    def __init__(self, size=4, score=0):
        self.size = size
        self.cells = None
        self.score = score
        self.reset()

    def reset(self):
        self.cells = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.add_random_item()
        self.add_random_item()

    def add_random_item(self):
        """ 空白区域随机生成一个2或4 """
        i, j = choice([(i, j) for i in range(self.size) for j in range(self.size) if self.cells[i][j] == 0])
        self.cells[i][j] = 4 if randrange(100) > 85 else 2

    def transpose(self):
        self.cells = [list(row) for row in zip(*self.cells)]

    def invert(self):
        self.cells = [row[::-1] for row in self.cells]

    # 移动合并
    def action_left(self, row):
        """ 向左合并 """
        def tighten(row):
            new_row = [i for i in row if i != 0]
            new_row += [0 for _ in range(len(row) - len(new_row))]
            return new_row

        def merge(row):
            pair = False
            new_row = []
            for i in range(len(row)):
                if pair:
                    new_row.append(2 * row[i])
                    self.score += 2 * row[i]
                    pair = False
                else:
                    if i + 1 < len(row) and row[i] == row[i + 1]:
                        pair = True
                        new_row.append(0)
                    else:
                        new_row.append(row[i])
            assert len(new_row) == len(row)
            return new_row

        return tighten(merge(tighten(row)))

    def move_left(self):
        self.cells = [self.action_left(row) for row in self.cells]

    def move_right(self):
        self.invert()
        self.move_left()
        self.invert()

    def move_up(self):
        self.transpose()
        self.move_left()
        self.transpose()

    def move_down(self):
        self.transpose()
        self.move_right()
        self.transpose()

    # 判断能不能移动
    @staticmethod
    def row_left(row):
        def change(i):
            if row[i] == 0 and row[i + 1] != 0:
                return True
            if row[i] != 0 and row[i + 1] != row[i]:
                return True
            return False
        return any(change(i) for i in range(len(row) - 1))

    def can_move_left(self):
        return any(self.row_left(row) for row in self.cells)

    def can_move_right(self):
        self.invert()
        can = self.can_move_left()
        self.invert()
        return can

    def can_move_up(self):
        self.transpose()
        can = self.can_move_left()
        self.transpose()
        return can

    def can_move_down(self):
        self.transpose()
        can = self.can_move_right()
        self.transpose()
        return can
