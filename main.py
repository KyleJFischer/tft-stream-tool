import numpy as np
from vidgear.gears import CamGear
import cv2

stream = CamGear(source='https://www.youtube.com/watch?v=QMh3jz3mZ2E', stream_mode = True, logging=True, options={"THREADED_QUEUE_MODE", False}).start() # YouTube Video URL as input
userActivePlacement = 0
template = cv2.imread('CrossedSwords.png',cv2.IMREAD_GRAYSCALE)
USER_PLACEMENT_X_CORD_TO_SEARCH = 1832
SENSITIVITY = 30
USER_FACING_X_CORD_TO_SEARCH = 1845
inPlaceColor = [0,0,0]

def getColorOfPoint(frame, x, y):
    return frame[y, x]

def likeColor(color1, color2):
    for i in range(3):
        if abs(color1[i] - color2[i]) > SENSITIVITY:
            return False
    return True

def findTemplateLocations(frame):
    # Apply template matching
    res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.1
    loc = np.where(res >= threshold)

    # Draw bounding boxes around template matches
    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (255, 0, 0), 2)

    return frame


def findPlayerPosition(frame):
    # Find health bar position for this color
    color_to_find = [48, 184, 226]
    # Replace with the color you want to find
    height, width, _ = frame.shape
    for y in range(210, height):
        pixel_color = getColorOfPoint(frame, USER_PLACEMENT_X_CORD_TO_SEARCH, y)
        if likeColor(pixel_color, color_to_find):
            return y
    return 0

def makeCross(frame, x = -1, y = -1, color=(0, 255, 0)):
    if x == -1 or y == -1:
        x = frame.shape[1] // 2
        y = frame.shape[0] // 2
 
    size = 7
    thickness = 2
    
    cv2.line(frame, (x - size, y), (x + size, y), color, thickness)
    cv2.line(frame, (x, y - size), (x, y + size), color, thickness)

def drawCrossOnUserPlacement(frame, x, y):
    makeCross(frame, USER_PLACEMENT_X_CORD_TO_SEARCH, y, (255, 255, 255))

def determineAndSetUserPlacement(yHeight):
    afterHeight = yHeight - 200
    print("AfterHeight: " + str(afterHeight))
    placeMent = int(afterHeight / 100 ) + 1
    print("PlaceMent: " + str(placeMent))
    userActivePlacement = placeMent

def doUserPlacementCode(frame):
    userY = findPlayerPosition(frame) 
    if (userY != -1):
        # Don't Do User Place 
        print("printUserY:" + str(userY))
        drawCrossOnUserPlacement(frame, USER_PLACEMENT_X_CORD_TO_SEARCH, userY)
        determineAndSetUserPlacement(userY) 

def doOpponentFacingCode(frame):
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    w, h = template.shape[::-1]
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

def processFrame(frame, yPlacement = -1):
    # getColorOfPoints(frame) 
    # placeCrossOnPixelsToTrack(frame)
    # drawGrid(frame)
    doUserPlacementCode(frame)
    doOpponentFacingCode(frame)
    # drawCrossOnUserPlacement(userY)
    # print(getColorOfPoint(frame, colorSamplingLocation[0], colorSamplingLocation[1]))
    # makeCross(frame, colorSamplingLocation[0], colorSamplingLocation[1], (255, 0, 0))
    
# infinite loop

framesToSkip = (stream.framerate / 10)

while True:
    frame = stream.read()
    # read frames
    if (framesToSkip > 0):
        framesToSkip -= 1
        continue
    framesToSkip = (stream.framerate / 1)
    # check if frame is None
    if frame is None:
        #if True break the infinite loop
        break
    
    
    processFrame(frame)
    
    cv2.imshow("Output Frame", frame)

    # Show output window
    key = cv2.waitKey(1) & 0xFF
    # check for 'q' key-press
    if key == ord("q"):
        #if 'q' key-pressed break out
        break
    

cv2.destroyAllWindows()
# close output window

# safely close video stream.
stream.stop()


def getColorOfPoint(frame, x, y):
    return frame[y, x]