import csv
import pygame

# The datasets are in .csv format, and contains the following info: 
# Timestamp (synchronized for all sensors) 
# Front video: object position, velocity, acceleration, classification
# 4 corner radars: object position, velocity, acceleration 
# ego vehicle information (‘our’ vehicle is called ego), such as velocity, acceleration, yaw rate, direction indicator status, and some more


# timestamp, object position, velocity, acceleration, classification
# timestamp, object position, velocity, acceleration
# timestamp, velcoity, acceleration, yaw rate, direction, indicator status

# objects = {
#  '12:30:33': {
#   'position': (1,2),
#   'velocity': 15,
#   'acceleration': 20,
#   'classification': ''
#  }
# }

# detect if the same object was detected by both the video sensor and the corner radars
def isObjectSame(obj1, obj2):
    return False

# get data from video sensor
# fill in the objects dictionary
def getDataFromVideoSensor(objects):
    print("getting data from video sensor")

# get data from corner radars
# fill in the objects dictionary if the object is not there already
def getDataFromCornerRadars(objects):
    # Now add the object or not 
    print("getting data from corner radar")

def combineObjects(videoObjects, cornerObjects): 
    allObjects = []
    return allObjects

def readDataFromDataSets(): 
    videoObjects = getDataFromVideoSensor()
    cornerObjects = getDataFromCornerRadars()
    ego = getEgoData()
    AllObjects = combineObjects(videoObjects, cornerObjects)
    return (ego, allObjects)

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)

def printText(win, text, font, color = (200,200,200), pos = (100,100)):
    render = font.render(text, 1, color)
    win.blit(render, pos)

def blit_text_center(win, font, text):
    render = font.render(text, 1, (200, 200, 200))
    blit_center(win, render)

def blit_center(win, render):
    win.blit(render, (win.get_width()/2 - render.get_width() / 2, win.get_height()/2 - render.get_height()/2))

def convertToPygame(win, x, y): 
    return (win.get_width() / 2 - y, win.get_height() / 2 - x)

def convertMetersToPixels(m, zoom):
    return m * 3 * zoom

def adjustPositionToObject(obj, x, y): 
    return ((x - obj.get_width() / 2), (y - obj.get_height() / 2))

def convertMeterPointToPygame(win, x, y, zoom):
    # 1 m = 1 * 3 * ZOOM
    pX = convertMetersToPixels(x,zoom)
    pY = convertMetersToPixels(y,zoom)

    return convertToPygame(win, pX, pY)

# ! Camera: 
    # * for each time stamp and for each object ID: 
        # ? object timestamp
        # ? object dx 
        # ? object dy 
        # ? object vx 
        # ? object vy
        # ? object type

# ! Corner Radars
    # * for each time stamp and for each object ID: 
        # ? object timestamp
        # ? object ax 
        # ? object ay
        # ? object dx
        # ? object dy
        # ? object dz
        # ? probObstacle 
        # ? object vx
        # ? object vy

# ! Camera Position 
    # ? posXCam
    # ? posYCam
    # ? posZCam

# camera_objects: [ # there are 15 objects 
#     "timestamp": {
#         new object(sdfdsf,sdfdsf,sdfdsf), 
#         new cyclist(){

#         }
#     }
# ]


# {
#     "sdfsdfs": 
# }


# Car
# Pedestrian
# Bike


# Ego = HOSTCAR




