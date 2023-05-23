class Cell:
    '''
    directions:
    1 2 3
    0 8 4
    7 6 5
    this is closed by mod 8
    '''

    directions = {1: (-1, -1), 2: (0, -1), 3: (1, -1),
                  0: (-1, 0), 8: (0, 0), 4: (1, 0),
                  7: (-1, 1), 6: (0, 1), 5: (1, 1)}

    def __init__(self, x, y, dir, type, energy):
        self.energy = energy
        self.type = type
        self.x = x
        self.y = y
        self.trend = dir % 8  # cell view direction
        self.get_vision_from_direction(self.trend)

    def get_vision_from_direction(self, main_direction):
        self.eyes = (
        (main_direction + 1) % 8, main_direction % 8, (main_direction + 7) % 8)  # directions that cell sees
        self.vision = [(self.x + Cell.directions[self.eyes[0]][0], self.y + Cell.directions[self.eyes[0]][1]),
                       (self.x + Cell.directions[self.eyes[1]][0], self.y + Cell.directions[self.eyes[1]][1]),
                       (self.x + Cell.directions[self.eyes[2]][0], self.y + Cell.directions[self.eyes[2]][
                           1])]  # coordinates that cell sees : [(x1,y1), (x2,y2), (x3,y3)]

    def get_objects_for_vision(self, objects):
        self.near_objects = [objects[self.vision[0][0]][self.vision[0][1]],
                             objects[self.vision[1][0]][self.vision[1][1]],
                             objects[self.vision[2][0]][self.vision[2][1]]]

    def action(self):
        return self.x, self.y, self.trend

    def rotate(self, direction):
        self.trend = direction % 8
        self.get_vision_from_direction(self.trend)
        self.action()

    def reproduction(self):
        '''in progress'''
        self.energy -= 2
        self.energy = self.energy // 2
        return self.x, self.y, dir, self.type, self.energy // 2


class Herbivore(Cell):
    type = 'herbivore'

    def __init__(self, x, y, dir, energy):
        super().__init__(x, y, dir, Herbivore.type, energy)

    def photosynthesis(self):
        self.energy += 1
        self.action()

    def move(self, idx_to_move):
        if isinstance(self.near_objects[idx_to_move], (Predator, Herbivore)):
            self.photosynthesis()
        else:
            self.x = self.vision[idx_to_move][0]
            self.y = self.vision[idx_to_move][1]
            self.action()


class Predator(Cell):
    type = 'predator'

    def __init__(self, x, y, dir, energy):
        super().__init__(x, y, dir, Predator.type, energy)

    def move(self, idx_to_move: int):
        '''idx_to_move = 0, 1, 2 - index of self.vision'''
        if isinstance(self.near_objects[idx_to_move], (Predator, Herbivore)):
            self.energy += 1
        else:
            self.energy -= 1

        self.x = self.vision[idx_to_move][0]
        self.y = self.vision[idx_to_move][1]

        self.action()
