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
    SCALING_VALUE = 3 * ZOOM
    def __init__(self, img, id, dx, dy, objectType, vx, vy, ax, ay, prob10bstacle, timestamp):
        self.id = id
        self.img = img
        self.dx = dx / 128 * self.SCALING_VALUE
        self.dy = dy / 128 * self.SCALING_VALUE 
        self.objectType = objectType
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay= ay
        self.prob10bstacle = prob10bstacle
        self.timestamp = timestamp

    def __key(self):
        return (self.dx, self.dy, self.objectType, self.vx, self.vy, self.ax, self.ay, self.prob10bstacle)
    def __hash__(self):
        return hash(self.__key())
    def __eq__(self, other):
        x1, y1 = self.dx / self.SCALING_VALUE, self.dy / self.SCALING_VALUE
        x2, y2 = other.dx / self.SCALING_VALUE, other.dy / self.SCALING_VALUE
        delta_x, delta_y = abs(x2 - x1), abs(y2 - y1)
        print((x1, y1), (x2, y2))
        return delta_x < 15 and delta_y < 15
        
    # def rotate(self, left=False, right=False):
    #     if left:
    #         self.angle += self.rotation_vel
    #     elif right:
    #         self.angle -= self.rotation_vel

    def draw(self, win):
        # blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
        currentX, currentY = convertToPygame(win, self.dx, self.dy)
        currentX, currentY = adjustPositionToObject(self.img, currentX, currentY)
        # currentX, currentY = adjustPositionToObject(self.img, self.dx, self.dy)
        # currentX, currentY = convertToPygame(win, currentX, currentY)
        win.blit(self.img, (currentX, currentY))

    # def move_forward(self):
    #     self.vel = min(self.vel + self.acceleration, self.max_vel)
    #     self.move()

    # def move_backward(self):
    #     self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
    #     self.move()

    # def move(self):
    #     radians = math.radians(self.angle)
    #     vertical = math.cos(radians) * self.vel
    #     horizontal = math.sin(radians) * self.vel

    #     self.y -= vertical
    #     self.x -= horizontal
    
    # def setxy(x, y):
    #     self.x += x
    #     self.y += x

    # def collide(self, mask, x=0, y=0):
    #     car_mask = pygame.mask.from_surface(self.img)
    #     offset = (int(self.x - x), int(self.y - y))
    #     poi = mask.overlap(car_mask, offset)
    #     return poi

    # def reset(self):
    #     self.x, self.y = self.START_POS
    #     self.angle = 0
    #     self.vel = 0

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
