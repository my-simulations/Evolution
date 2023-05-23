import numpy as np

class Field:
    def __init__(self):
        self.field = np.zeros(2704)
        self.field = self.field.reshape(52, 52)
        # 0 - floor, 1 - wall, 2 - herbivore, 3 - predator
        self.field[0, :] += 1
        self.field[:, 0] += 1
        self.field[-1, :] += 1
        self.field[:, -1] += 1
        print('field init')

    def cell_step(self, type, x_start, y_start, x_finish, y_finish):
        self.field[x_start, y_start] = 0
        self.field[x_finish, y_finish] = type

    def get_info(self):
        return self.field


a = Field()
b = a.get_info()
print(type(b))
print(len(b))
for x in range(len(b)):
    for y in range(len(b)):
        print(x, y, b[x][y])