import pygame
import time
import math
from utils import *
from models import *
from constants import *
from csvReader import *
pygame.font.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
ORIGIN_X, ORIGIN_Y = WIN.get_width()/2, WIN.get_height()/2
pygame.display.set_caption("Automotive stimulation!!")
MAIN_FONT = pygame.font.SysFont("comicsans", 44)
FPS = 60

def draw(win, images, objects):
    for img, pos in images:
        win.blit(img, pos)

    for obj in objects:
        obj.draw(win)
    pygame.display.update()

run = True
clock = pygame.time.Clock()
images = [(GREEN_BACKGROUND, (0, 0))]
game_info = GameInfo()
HOST_CAR_OBJECT = AbstractObject(scale_image(CAR, ZOOM/4), -1, 0, 0,-1,-1,-1,-1,-1,-1,-1)
while not game_info.started:
    draw(WIN, images, [])
    blit_text_center(
        WIN, MAIN_FONT, f"Start ROAD_BACKGROUND")
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

        if event.type == pygame.KEYDOWN:
            game_info.start()

for timestamp in corner0_objects:
    print(timestamp)
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            game_info.finish()
            exit()
            break

    objs = []
    for obj in camera_objects[timestamp]:
        objs.append(obj)
    for obj in corner0_objects[timestamp]:
        objs.append(obj)
    for obj in corner1_objects[timestamp]:
        objs.append(obj)
    for obj in corner2_objects[timestamp]:
        objs.append(obj)
    for obj in corner3_objects[timestamp]:
        objs.append(obj)
    unique_objs = objs
    for obj in unique_objs:
        obj.draw(WIN)
        pygame.display.update()
        
    
    draw(WIN, images, [HOST_CAR_OBJECT])

pygame.quit()