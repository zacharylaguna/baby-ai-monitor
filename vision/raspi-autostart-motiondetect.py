import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import requests
 
contourlist = []
activated = False
motion = False
 
# defining a function to calculate mode. It
# takes list variable as argument
def mode(lst):
 
	# creating a dictionary
	freq = {}
	for i in lst:
 
		# mapping each value of list to a
		# dictionary
		freq.setdefault(i, 0)
		freq[i] += 1
 
	# finding maximum value of dictionary
	hf = max(freq.values())
 
	# creating an empty list
	hflst = []
 
	# using for loop we are checking for most
	# repeated value
	for i, j in freq.items():
		if j == hf:
			hflst.append(i)
 
	# returning the result
	return hflst
 
def sendImage():
    try:
        url = 'http://www.dev-machine.link:5000/upload_image'
        my_img = {'image': open('image.jpg', 'rb')}
        r = requests.post(url, files=my_img)
    except Exception as e:
        print('error sending')
 
def activateAlert():
    print('activated')
    try:
        r = requests.get('http://dev-machine.link:5000/activate')
    except Exception as e:
        print('error sending')
    # print(r.status_code)
 
def deactivateAlert():
    print('deactivated')
    try:
        r = requests.get('http://dev-machine.link:5000/deactivate')
    except Exception as e:
        print('error sending')
    # print(r.status_code)
 
def activateMotion():
    print('motion')
    try:
        r = requests.get('http://dev-machine.link:5000/activateMotion')
    except Exception as e:
        print('error sending')
    # print(r.status_code)
 
def deactivateMotion():
    print('no motion')
    try:
        r = requests.get('http://dev-machine.link:5000/deactivateMotion')
    except Exception as e:
        print('error sending')
    # print(r.status_code)
 
# PERSPECTIVES = ('TOP', 'SIDE')
perspective = 'SIDE' # side is default
def borderalarm(x, y, w, h, width, height):
    global activated
    global perspective
    # is motion near the edge of camera?
    # print(activated)
    midpoint = ((x+(x+w))/2, (y+(y+h))/2)
    if midpoint[0] < width / 6.0 or midpoint[0] > (5*width / 6.0): # midpoint is [0,width/8) or (7/8 * width, width]
        if activated == False:
            activateAlert()
            activated = True
        # print('activated', midpoint)
    elif midpoint[1] < height / 6.0: # midpoint is [0,height/8) or (7/8 * height, height]
        if activated == False:
            activateAlert()
            activated = True
        # print('activated', midpoint)
    elif midpoint[1] > (5*height / 6.0) and perspective == 'TOP': # only include bottom section if from TOP perspective
        if activated == False:
            activateAlert()
            activated = True
    else:
        if activated == True:
            deactivateAlert()
            activated = False
        # print('deactivated', midpoint)
 
def motionDetection():
    global activated
    global contourlist
    global motion
    cap = cv.VideoCapture(0)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
 
    imagenumber = 0
 
    while cap.isOpened():
        diff = cv.absdiff(frame1, frame2)
        diff_gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(diff_gray, (5, 5), 0)
        _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
        dilated = cv.dilate(thresh, None, iterations=3)
        contours, _ = cv.findContours(
            dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
 
        for contour in contours:
            (x, y, w, h) = cv.boundingRect(contour)
            # added to smooth the motion
            contourlist.append(cv.contourArea(contour))
            avg = 0
            if len(contourlist) >= 500:
                contourlist.pop(0)
                avg = sum(contourlist) / len(contourlist)
            # done adding
            # if level of motion is UNDER threshold
            threshold = 900
            if cv.contourArea(contour) < threshold:
                continue
 
            # if level of motion is OVER threshold
            if avg < threshold:
                if motion == True:
                    deactivateMotion()
                    motion = False
            else:
                if motion == False:
                    activateMotion()
                    motion = True
 
            # is motion near the edge of camera?
            # Get the height and width of the provided video frame
            height = frame1.shape[0]
            width = frame1.shape[1]
            borderalarm(x, y, w, h, width, height)
 
            cv.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv.FONT_HERSHEY_SIMPLEX,
                       1, (255, 0, 0), 3)
 
        # cv.drawContours(frame1, contours, -1, (0, 255, 0), 2)
 
        #cv.imshow("Video", frame1)
        cv.imwrite('image.jpg', frame1)
        sendImage()
        frame1 = frame2
        ret, frame2 = cap.read()
 
        if cv.waitKey(50) == 27:
            break
 
    cap.release()
    cv.destroyAllWindows()
 
if __name__ == "__main__":
    # perspective = input('please input perspective (TOP or SIDE):').upper()
    # if perspective not in PERSPECTIVES:
        # print('did not choose TOP or SIDE')
        # quit()
    x=True
    while True:
        try:
            if x == True:
                deactivateAlert()
            motionDetection()
            x = False
        except Exception as e:
            f = open('debug.txt','a')
            f.write('hi')
            f.close()