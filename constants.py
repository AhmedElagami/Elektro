from utils import *

# it's set to 1x to show everything
# for zoomed view set it to 4
ZOOM = 4
CAR = scale_image(pygame.image.load("imgs/car_400.png"), ZOOM/4)
BACKGROUND = pygame.image.load("imgs/background.jpg")
ROAD_BACKGROUND = pygame.image.load("imgs/road_background.jpg")
BLUE_BACKGROUND = pygame.image.load("imgs/blue_background.png")
UNKNOWN = scale_image(pygame.image.load("imgs/unknown_400.png"), ZOOM/4)
PEDESTRIAN = scale_image(pygame.image.load("imgs/pedestrian_400.png"), ZOOM/4)
BIKE = scale_image(pygame.image.load("imgs/bike_400.png"), ZOOM/4)
EGO = scale_image(pygame.image.load("imgs/ego_400.png"), ZOOM/4)
BLIND = scale_image(pygame.image.load("imgs/blind_400.png"), ZOOM/4)


WIDTH, HEIGHT = BLUE_BACKGROUND.get_width(), BLUE_BACKGROUND.get_height()