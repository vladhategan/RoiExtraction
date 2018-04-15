import cv2
import numpy as np
import datetime as dt
import math


'''
this is a recursive function that labels every object
it recursively checks the neighbours (4 degree neighbourhood) of each pixel and assign a label to that pixel
if none of the conditions are true the function exits the recurssion and the program looks for another object to label
'''

def labelObj(img, i, j, label, centerMat):
    if((i+1 != img.shape[0]) and (img[i+1,j] == 255)):
        img[i+1, j] = label

        centerMat[0, label] += i+1
        centerMat[1, label] += j
        centerMat[2, label] +=1
        labelObj(img, i+1, j, label, centerMat)
    if((i-1 != 0) and (img[i-1,j] == 255)):
        img[i-1, j] = label
        centerMat[0, label] += i-1

        centerMat[1, label] += j
        centerMat[2, label] +=1
        labelObj(img, i-1, j, label, centerMat)
    if((j+1 != img.shape[1]) and (img[i,j+1] == 255)):
        img[i, j+1] = label

        centerMat[0, label] += i
        centerMat[1, label] += j+1
        centerMat[2, label] +=1
        labelObj(img, i, j+1, label, centerMat)
    if((j-1 != 0) and (img[i,j-1] == 255)):
        img[i, j-1] = label

        centerMat[0, label] += i
        centerMat[1, label] += j-1
        centerMat[2, label] +=1
        labelObj(img, i, j-1, label, centerMat)






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
obtain height and width of the image
centerMat is a frequency matrix, 3x2
on the first row firs col it holds the  row indices
on the second row first col it holds the col indices
on the third row first col it holds the frequency of that labels
on the second row it holds the object number (label)
'''
height = cont_img.shape[0]
width = cont_img.shape[1]
label = 1
centerMat = np.zeros((3,255), np.uint32)


labels = []
'''
iterate over the image and label every object
'''
for i in range(0, height):
    for j in range(0, width):
        if(cont_img[i,j] == 255):
            cont_img[i,j] = label
            centerMat[0, label] += i
            centerMat[1, label] += j
            centerMat[2, label] +=1
            labelObj(cont_img, i,j, label, centerMat)
            labels.append(label)
            label+=1

'''
in points we save coordinated of mass centers of each object
in colors we hold the color of every mass center
'''
points = []
colors = []
for i in range(0, 255):
    if(centerMat[2, i]):
        points.append((int(centerMat[0,i]/centerMat[2,i]), int(centerMat[1,i]/centerMat[2,i])))
        colors.append(img[int(centerMat[0,i]/centerMat[2,i]), int(centerMat[1,i]/centerMat[2,i])])
        #cv2.circle(img,(int(centerMat[1,i]/centerMat[2,i]), int(centerMat[0,i]/centerMat[2,i])), 6, (0,0,255), -1)

'''
sort centers of mass and write them to a file
'''
points.sort(key=lambda tup: tup[0])
print(points)
print(labels)
print(colors)

leds = open('leds.txt', 'w')

leds.write("center points: ")
leds.write(str(points))
leds.write("\n")

leds.write("labels: ")
leds.write(str(labels))
leds.write("\n")

leds.write("colors: ")
leds.write(str(colors))
leds.write("\n")

leds.close()

'''
draw a red circle with the center in the center of mass of each object
'''
for i in points:
    cv2.circle(img,(i[1],i[0]   ), 6, (0,0,255), -1)
cv2.imshow("final", img)
cv2.waitKey(0)








'''
im2, contours, hierarchy = cv2.findContours(cont_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#im2, contours, hierarchy = cv2.findContours(cont_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    area = cv2.contourArea(cnt)
    print(cnt)

    if area > 40:
        continue

    ellipse = cv2.fitEllipse(cnt)
    cv2.ellipse(img, ellipse, (0,255,0), 2)

cv2.imshow("roi", img);
cv2.waitKey(0)
'''
