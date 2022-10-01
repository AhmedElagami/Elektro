import pygame
import time
import math
from utils import *
from models import *
from constants import *
from csvReader import *
import cv2

pygame.font.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
ORIGIN_X, ORIGIN_Y = WIN.get_width()/2, WIN.get_height()/2
pygame.display.set_caption("Automotive stimulation!!")
MAIN_FONT = pygame.font.SysFont("comicsans", 24)
SECOND_FONT = pygame.font.SysFont("comicsans", 12)
BLIND_LEFT_REC_POINT = convertMeterPointToPygame(WIN, 0.85 - 1, 1.55, ZOOM)
BLIND_RIGHT_REC_POINT = convertMeterPointToPygame(WIN, 0.85 - 1, -1.55, ZOOM)
REC_WIDTH_PIXELS = convertMetersToPixels(10, ZOOM)
REC_HEIGHT_PIXELS = convertMetersToPixels(2.3, ZOOM)
BLIND_RECT_LEFT = pygame.Rect(BLIND_LEFT_REC_POINT[0] - REC_WIDTH_PIXELS/2, BLIND_LEFT_REC_POINT[1] - REC_HEIGHT_PIXELS/2, REC_WIDTH_PIXELS, REC_HEIGHT_PIXELS)
BLIND_RECT_RIGHT = pygame.Rect(BLIND_RIGHT_REC_POINT[0] - REC_WIDTH_PIXELS/2, BLIND_RIGHT_REC_POINT[1] - REC_HEIGHT_PIXELS/2, REC_WIDTH_PIXELS, REC_HEIGHT_PIXELS)

VIDEO = cv2.VideoCapture('video.avi')
success, video_image = VIDEO.read()
# VIDEO.set(cv2.CAP_PROP_FPS, int(10))

# FPS = VIDEO.get(cv2.CAP_PROP_FPS)
FPS = 30

FRAME_COUNTER_MAX = 2
video_frame_counter = FRAME_COUNTER_MAX
current_video_surf = pygame.transform.scale(pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR"), (400, 300))

def drawVideoSurf(win, video_surf):
    win.blit(video_surf, (940, 30))

def drawVideo(win, video):
    global current_video_surf
    success, video_image = video.read()
    if success:
        video_surf = pygame.transform.scale(pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR"), (400, 300))
        current_video_surf = video_surf
        drawVideoSurf(win, video_surf)

def draw(win, images, objects):
    global video_frame_counter
    for img, pos in images:
        win.blit(img, pos)

    pygame.draw.rect(WIN, (115, 143, 157), BLIND_RECT_LEFT)
    pygame.draw.rect(WIN, (115, 143, 157), BLIND_RECT_RIGHT)

    printText(WIN,"Timestamp: ", MAIN_FONT, pos=(50,50*ZOOM/2))
    printText(WIN,"Ego: ", MAIN_FONT, pos=(50,85*ZOOM/2))
    printText(WIN,"Car: ", MAIN_FONT, pos=(50,120*ZOOM/2))
    printText(WIN,"Bike: ", MAIN_FONT, pos=(50,155*ZOOM/2))
    printText(WIN,"Pedestrian: ", MAIN_FONT, pos=(50,185*ZOOM/2))
    printText(WIN,"UNKNOWN: ", MAIN_FONT, pos=(50,220*ZOOM/2))
    printText(WIN,"BLIND: ", MAIN_FONT, pos=(50,255*ZOOM/2))

    pygame.draw.line(win, (200,0,0),(0,WIN.get_height()/2),(WIN.get_width(), WIN.get_height()/2))
    pygame.draw.line(win, (200,0,0),(WIN.get_width()/2,0),(WIN.get_width()/2, WIN.get_height()))

    for obj in objects:
        cX, cY = obj.draw(win, False)
        printText(WIN, str(obj.getXYfromOriginInMeters()),SECOND_FONT, (0,200,0), (cX, cY))

    if (video_frame_counter == FRAME_COUNTER_MAX):
        drawVideo(win, VIDEO)
        video_frame_counter = 0
    else:
        drawVideoSurf(win, current_video_surf)
        video_frame_counter += 1

    pygame.display.update()

run = True
clock = pygame.time.Clock()
images = [(BLUE_BACKGROUND, (0, 0)), (EGO, (200, 85*ZOOM/2)), (CAR, (200, 120*ZOOM/2)), (BIKE, (200, 155*ZOOM/2)), (PEDESTRIAN, (200, 185*ZOOM/2)), (UNKNOWN, (200, 220*ZOOM/2)), (BLIND, (200, 255*ZOOM/2))]
game_info = GameInfo()
HOST_CAR_OBJECT = AbstractObject(EGO, -1, 0, 0,7,-1,-1,-1,-1,-1,-1)

draw(WIN, images, [])
blit_text_center(
    WIN, MAIN_FONT, f"Start Simulation")
pygame.display.update()

def isInBlindSpot(win,obj, rec):
    oldX, oldY = convertToPygame(win, obj.dx, obj.dy)
    currentX, currentY = adjustPositionToObject(obj.img, oldX, oldY)
    obj_rect = obj.img.get_rect(topleft = (currentX, currentY))
    if rec.colliderect(obj_rect):
        printText(WIN,"A CAR ENTERED BLIND SPOT", MAIN_FONT, color = "red", pos=(50,650))
        return True;
    return False

while not game_info.started:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

        if event.type == pygame.KEYDOWN:
            game_info.start()

# it doesn't matter what array we use cuz they have the same keys anyway
skip = False
for timestamp in corner0_objects:
    if (skip == True):
        skip = False
        continue
    skip = True
    # controlling the FPS
    clock.tick(FPS)

    # checking if you're closing the app
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            game_info.finish()
            exit()
            break

    # holds the current objects detected by all sensors
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

    # removing duplicate objects 
    objs.sort(key=lambda x: x.getXYfromOriginInMeters())

    unique_objs = []
    for obj in objs:
        if obj not in unique_objs:
            unique_objs.append(obj)

    cX, cY = 0,0
    for obj in unique_objs:
        if (obj.dx == 0 and obj.dy == 0):
            continue
        isBlind = (isInBlindSpot(WIN, obj, BLIND_RECT_LEFT) or isInBlindSpot(WIN, obj, BLIND_RECT_RIGHT))
        cX, cY = obj.draw(WIN,isBlind)
        printText(WIN, str(obj.getXYfromOriginInMeters()),SECOND_FONT, (0,200,0), (cX, cY))

    # predicting next objects positions

    printText(WIN,"Timestamp: " + timestamp, MAIN_FONT, pos=(50,50*ZOOM/2))
    pygame.display.update()
    # reseting the screen, by drawing the background and Ego
    draw(WIN, images, [HOST_CAR_OBJECT])

    # viewing the video 

pygame.quit()

# ! for each timestamp:
    # * get current objects 
    # * remove duplicate objects 
    # * add them to the prediction list
    # * predict their next values

    # TODO NEXT
    # ? get current objects
    # ? remove duplicate objects
    # ? Are the predicted objects there in the current ones> 
        # ! if there aren't:
            # * check if they are too far
            # * or they are in the blind spot:
                # * if they are, keep the uncommon ones in the predicted list 
                # * then change them to 
                        # ! RED
        # ! if there are:
            # * remove the common ones from the predicted list 
            # * add the unique list
    # ? draw the predicted list
    # ? predict the next values
    # ? repeat
