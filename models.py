from utils import *
from constants import *

class GameInfo:
    def __init__(self):
        self.finished = False
        self.started = False

    def reset(self):
        self.started = False
        self.finished = False

    def finish(self): 
        self.finished = True

    def start(self):
        self.started = True
    
    def game_finished():
        return self.finished

class AbstractObject:
    X_SCALING_VALUE = 3 * ZOOM
    Y_SCALING_VALUE = 3 * ZOOM
    def __init__(self, img, id, dx, dy, objectType, vx, vy, ax, ay, prob10bstacle, timestamp):
        self.id = id
        self.img = img
        self.dx = dx / 128 * self.X_SCALING_VALUE
        self.dy = dy / 128 * self.Y_SCALING_VALUE 
        self.objectType = objectType
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay= ay
        self.prob10bstacle = prob10bstacle
        self.timestamp = timestamp
        self.setImage()
    def __key(self):
        return (self.dx, self.dy, self.objectType, self.vx, self.vy, self.ax, self.ay, self.prob10bstacle)
    def __hash__(self):
        return hash(self.__key())
    def __eq__(self, other):
        x1, y1 = self.getXYfromOriginInMeters()
        x2, y2 = other.getXYfromOriginInMeters()
        delta_x, delta_y = abs(x2 - x1), abs(y2 - y1)
        return delta_x <= 5.5 and delta_y <= 3

    def draw(self, win, isBlind):
        if (self.dx != 0 and self.dy != 0) and isBlind:
            print("blind spot")
            self.img = BLIND
        else: 
            self.setImage()
        oldX, oldY = convertToPygame(win, self.dx, self.dy)
        currentX, currentY = adjustPositionToObject(self.img, oldX, oldY)
        win.blit(self.img, (currentX, currentY))
        return oldX, oldY
    
    def getXYfromOriginInMeters(self):
        return ((self.dx / self.X_SCALING_VALUE), (self.dy / self.Y_SCALING_VALUE))
    
    def setImage(self):
        if self.objectType == 1 or self.objectType == 2 or self.objectType == 6: 
            self.img = CAR
        elif self.objectType == 3 or self.objectType == 4:
            self.img = BIKE
        elif self.objectType == 5:
            self.img = PEDESTRIAN
        elif self.objectType == 6:
            self.img = EGO



# class Ego(AbstractObject):
#     img = CAR
#     START_POS = (ORIGIN_X - CAR.get_width() / 2, ORIGIN_Y - CAR.get_height()/2)


#     # def __init__(self, img, rotation_vel):
#     def __init__(self):
#         super().__init__(CAR, 0)
#         self.direction_indicator = False
#         self.yaw_rate = 1

#     def reduce_speed(self):
#         self.vel = max(self.vel - self.acceleration / 2, 0)
#         self.move()

#     def bounce(self):
#         self.vel = -self.vel
#         self.move()

# class Pedestrian(AbstractObject):
#     img = PEDESTRIAN
#     START_POS = (180, 200)
#     # def __init__(self, img, rotation_vel):
#     def __init__(self):
#         super().__init__(self.img, 0)
#         self.direction_indicator = False
#         self.yaw_rate = 1

#     def reduce_speed(self):
#         self.vel = max(self.vel - self.acceleration / 2, 0)
#         self.move()

#     def bounce(self):
#         self.vel = -self.vel
#         self.move()

# class Cyclist(AbstractObject):
#     img = BIKE
#     START_POS = (180, 200)
#     # start_pos = calcPositionToOrigin()

#     def __init__(self):
#         super().__init__(self.img, 0)
#         self.direction_indicator = False
#         self.yaw_rate = 1
