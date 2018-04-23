import cv2
import numpy as np
import datetime as dt
import math

#horrible estimate
def checkYAxis(y):
    if 100<y<240:
        return 1
    if 240<y<326:
        return 2
    if 326<y<400:
        return 3
    if 400<y<490:
        return 4
    if 490<y<530:
        return 5
    if 530<y<620:
        return 6

def checkLed(xval, yval, med, img, r):

    if img[xval, yval-med] == 1 and yval-med !=0:

        #print('a')
        #print(r)
        r += 1
        return checkLed(xval, yval-med, med, img, r)

    return r

'''
read the immage and apply gray filter
'''
img = cv2.imread('Clipboard02.bmp')
cv2.imshow("image", img)
cv2.waitKey(0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

'''
apply gaussian blur to the gray image
'''
gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)
cv2.imshow("gas", gray_blur)
cv2.waitKey(0)

'''
binarize the image with 200 threshold
thresh1 is the binarized image
'''
ret,thresh1 = cv2.threshold(gray_blur,200,255,cv2.THRESH_BINARY)
cv2.imshow("gas", thresh1)
cv2.waitKey(0)

'''
compute the closing using a 3x3 kernel
'''

kernel = np.ones((3,3), np.uint8)
closing = cv2.morphologyEx(thresh1, cv2.MORPH_CLOSE,kernel,iterations=4)
cv2.imshow("gas4", closing)
cv2.waitKey(0)

'''
we'll work on a copy of the processed image
'''
cont_img = closing.copy()

'''
find the contours
'''
im2,ctrs, hier = cv2.findContours(cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * img.shape[1] ) (left to right top to bottom)

'''
sort the contours from left to right
'''
sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
centroids = []
on_leds = []
y_values = []

for i, ctr in enumerate(sorted_ctrs):
    # Get bounding box
    x, y, w, h = cv2.boundingRect(ctr)


    #Centroids coordinates
    M = cv2.moments(ctr)
    cY = int(M["m10"] / M["m00"])
    cX = int(M["m01"] / M["m00"])
    centroids.append((cX,cY))

    #save Y values for sorting
    y_values.append(cY)


    #test = checkYAxis(cY)
    #on_leds.append(test)

    #cv2.drawContours(img, [ctr], -1, (0, 255, 0), 2)
    #cv2.rectangle(img,(x,y),( x + w, y + h ),(90,0,255),2)
    #cv2.putText(img, str(test), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

print("y axis values: ")
print(y_values)
m = []
med = 0

#compute the average value for all the y axis values
if len(y_values) > 1:
    for i in range(0, len(y_values)-1):
        m.append(y_values[i+1]-y_values[i])
    for elem in m:
        med += elem
    med /= len(m)

leds = open('leds2.txt', 'w')
#go through contours again and draw bounding rectangles and the sequence numbers for each rectangle
for i, ctr in enumerate(sorted_ctrs):
    # Get bounding box
    x, y, w, h = cv2.boundingRect(ctr)
    M = cv2.moments(ctr)
    cY = int(M["m10"] / M["m00"])
    cX = int(M["m01"] / M["m00"])
    cv2.rectangle(img,(x,y),( x + w, y + h ),(90,0,255),2)

    if len(y_values) == 1:
        cv2.putText(img, "1", (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
        leds.write("led 1 is on ")
    else:
        test = checkLed(cX, cY, med, cont_img, 1)
        on_leds.append(test)
        cv2.putText(img, str(test), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

leds.write("On leds: ")
leds.write(str(on_leds))
leds.close()

cv2.imshow('marked areas',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
print("Centroids:")
print (centroids)
print ("Number of Contours -> %d "%len(ctrs))
print("on leds:")
print (on_leds)
'''
TODO: iterate through Y values of centroids
and find median value of (c2 - c1) (c3-c2)...
use that as the estimate for which led is open
'''



# define the list of boundaries
# Convert to HSV colorspace
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#Yellow
lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
upper_yellow = np.array([40, 255, 255], dtype=np.uint8)
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

output = cv2.bitwise_and(img, img, mask = mask)
cv2.imshow("images",output)
cv2.waitKey(0)






'''
output = cv2.connectedComponents(cont_img, 4, cv2.CV_32S)


num_labels = output[0]
labels = output[1]



cnts = cv2.findContours(cont_img, cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = contours.sort_contours(cnts)[0]




# Map components labels to hue val
label_hue = np.uint8(179*labels/np.max(labels))
blank_ch = 255*np.ones_like(label_hue)
labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

#cvt to bgr display
labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

#set bg label to black
labeled_img[label_hue==0] = 0
cv2.imshow("labeled", labeled_img)
cv2.waitKey(0)
'''
