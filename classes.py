from brain import *


class Cell:
    '''
    directions:
    3 2 1
    4 8 0
    5 6 7
    this is closed by mod 8
    '''

    directions = {3: (-1, 1), 2: (0, 1), 1: (1, 1),
                  4: (-1, 0), 8: (0, 0), 0: (1, 0),
                  5: (-1, -1) , 6: (0, -1), 7: (1, -1)}

    def __init__(self, x, y, type, dir, energy):
        self.energy = energy
        self.type = type
        self.x = x
        self.y = y
        self.trend = dir % 8  # cell view direction
        self.get_vision_from_direction(self.trend)

    def get_vision_from_direction(self, main_direction):
        self.eyes = ((main_direction + 1) % 8, main_direction % 8, (main_direction + 7) % 8)  # directions that cell sees
        self.vision = [(self.x + Cell.directions[self.eyes[0]][0], self.y + Cell.directions[self.eyes[0]][1]),
                       (self.x + Cell.directions[self.eyes[1]][0], self.y + Cell.directions[self.eyes[1]][1]),
                       (self.x + Cell.directions[self.eyes[2]][0], self.y + Cell.directions[self.eyes[2]][1])]  # coordinates that cell sees : [(x1,y1), (x2,y2), (x3,y3)]

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

    type = 2

    def __init__(self, x, y, dir, energy):
        super().__init__(x, y, Herbivore.type, dir, energy)
        self.brain = network(self.type)

    def photosynthesis(self):
        self.energy += 1
        self.action()

    def move(self, idx_to_move):
        '''idx_to_move = 0, 1, 2 - index of self.vision'''
        if self.near_objects[idx_to_move] in set(1, 2, 3):
            self.photosynthesis()
        else:
            self.x = self.vision[idx_to_move][0]
            self.y = self.vision[idx_to_move][1]
            self.action()
    
    def think(self, time):
        data0 = np.zeros(14)
        data0[self.near_objects[0]] = 1
        data0[self.near_objects[1] + 4] = 1
        data0[self.near_objects[2] + 4*2] = 1
        data0[-2] = self.energy
        data0[-1] = np.sin(time)

        res = self.brain.forward(data0)

        return res
    
    def step(self, time):
        p, dir = self.think(time)
        steps_ids = np.argsort(p)[::-1]

        for step_id in steps_ids:

            if step_id in set(0, 1, 2):
                if res := self.move(step_id):
                    return res
                else:
                    next
            
            elif step_id == 3:
                return self.rotate(dir)

            elif step_id == 4:
                if res := self.reproduction():
                    return res
                else:
                    next
                    
            elif step_id == 5:
                return self.photosynthesis()





class Predator(Cell):

    type = 3

    def __init__(self, x, y, dir, energy):
        super().__init__(x, y, Predator.type, dir, energy)
        self.brain(self.type)

    def move(self, idx_to_move: int):
        '''idx_to_move = 0, 1, 2 - index of self.vision'''
        if self.near_objects[idx_to_move] in set(2, 3):
            self.energy += 1
        elif self.near_objects[idx_to_move] == 1:
            return
        else:
            self.energy -= 1

        self.x = self.vision[idx_to_move][0]
        self.y = self.vision[idx_to_move][1]

        self.action()
    
    def think(self, time):
        data0 = np.zeros(14)
        data0[self.near_objects[0]] = 1
        data0[self.near_objects[1] + 4] = 1
        data0[self.near_objects[2] + 4*2] = 1
        data0[-2] = self.energy
        data0[-1] = np.sin(time)

        res = self.brain.forward(data0)

        return res
    
    def step(self, time):
        p, dir = self.think(time)
        steps_ids = np.argsort(p)[::-1]

        for step_id in steps_ids:

            if step_id in set(0, 1, 2):
                if res := self.move(step_id):
                    return res
                else:
                    next
            
            elif step_id == 3:
                return self.rotate(dir)

            elif step_id == 4:
                if res := self.reproduction():
                    return res
                else:
                    next


class Wall:

    type = 1
    
    def __init__(self):
        self.type = Wall.type