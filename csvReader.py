import csv
from constants import *
from models import AbstractObject

# {
#     "timestamp": {
#         "id":0,
#         "dx": 10,
#         "dy": 10,
#         "objectType": "car", 
#         "vx": 10, 
#         "vy": 10,
#     },
# }

# {
#   "timestamp": [
        # {
    #         "id":0,
    #         "timestamp": "dsfsd"
    #         "ax": 10,
    #         "ay": 10,
    #         "dx": 10,
    #         "dy": 10,
    #         "dz": 10,
    #         "prob10bstacle": 10,
    #         "vx": 10, 
    #         "vy": 10,
    #     },
   #]
# }

# {
#     "timestamp": {
        # "posXCam": ""
        # "posYCam": ""
        # "posZCam": ""
#     },
# }


camera_objects = {}
corner0_objects = {}
corner1_objects = {}
corner2_objects = {}
corner3_objects = {}

def getObjectIdFromColumnName(col):
    if "cornerData" in col:
        return int(col[163])
    elif "camData" in col:
        if col[148].isdigit():
            return int(col[147] + col[148])
        return int(col[147])

def addInfoFromRow(sensor, row, noOfObjects, dataset):
    tempHeaderName = ""
    if sensor == "camera":
        tempHeaderName = f"_g_Infrastructure_CCR_NET_NetRunnablesClass_m_rteInputData_out_local.TChangeableMemPool._._._m_arrayPool._0_._elem._m_camData._m_objects._m_value."
    elif sensor == "corner0":
        tempHeaderName = f"_g_Infrastructure_CCR_NET_NetRunnablesClass_m_rteInputData_out_local.TChangeableMemPool._._._m_arrayPool._0_._elem._m_cornerData._m_value._0_._m_objects._m_value."
    elif sensor == "corner1":
        tempHeaderName = f"_g_Infrastructure_CCR_NET_NetRunnablesClass_m_rteInputData_out_local.TChangeableMemPool._._._m_arrayPool._0_._elem._m_cornerData._m_value._1_._m_objects._m_value."
    elif sensor == "corner2":
        tempHeaderName = f"_g_Infrastructure_CCR_NET_NetRunnablesClass_m_rteInputData_out_local.TChangeableMemPool._._._m_arrayPool._0_._elem._m_cornerData._m_value._2_._m_objects._m_value."
    elif sensor == "corner3":
        tempHeaderName = f"_g_Infrastructure_CCR_NET_NetRunnablesClass_m_rteInputData_out_local.TChangeableMemPool._._._m_arrayPool._0_._elem._m_cornerData._m_value._3_._m_objects._m_value."
    i = 0
    timestamp = row['t']
    if timestamp not in dataset:
        dataset[timestamp] = []
    while i < noOfObjects:
        headerName = tempHeaderName + "_" +  str(i) + "_._m_"

        dx = int(row[headerName + 'dx'])
        # _g_Infrastructure_CCR_NET_NetRunnablesClass_m_rteInputData_out_local.TChangeableMemPool._._._m_arrayPool._0_._elem._m_cornerData._m_value._0_._m_objects._m_value._0_._m_dx
        # _g_Infrastructure_CCR_NET_NetRunnablesClass_m_rteInputData_out_local.TChangeableMemPool._._._m_arrayPool._0_._elem._m_cornerData._m_value._0_._m_objects._m_value._10_._m_dx
        dy = int(row[headerName + 'dy'])
        vx = int(row[headerName + "vx"])
        vy = int(row[headerName + "vy"])
        ax = -1
        ay = -1
        dz = -1
        prob1Obstacle = -1
        if "corner" in sensor:
            ax = int(row[headerName + 'ax'])
            ay = int(row[headerName + 'ay'])
            dz = int(row[headerName + 'dz'])
            objectType = -1 # because it's corner data
            prob1Obstacle = int(row[headerName + 'prob1Obstacle'])
        else:
            objectType = int(row[headerName + 'objType'])
        
        img = scale_image(UNKNOWN, ZOOM/4)
        if objectType == 1 or objectType == 2 or objectType == 6: 
            img = scale_image(CAR, ZOOM/4)
        elif objectType == 3 or objectType == 4:
            img = scale_image(BIKE, ZOOM/4)
        elif objectType == 5:
            img = scale_image(PEDESTRIAN, ZOOM/4)
        currentObject = AbstractObject(img, i, dx, dy, objectType, vx, vy, ax, ay, prob1Obstacle, timestamp)
        dataset[timestamp].append(currentObject)
        i += 1

with open('data.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        addInfoFromRow("camera", row, 14, camera_objects)
        addInfoFromRow("corner0", row, 10, corner0_objects)
        addInfoFromRow("corner1", row, 10, corner1_objects)
        addInfoFromRow("corner2", row, 10, corner2_objects)
        addInfoFromRow("corner3", row, 10, corner3_objects)

print("Done taking data")
