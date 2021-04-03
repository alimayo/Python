

import numpy as np
import cv2
from google.colab.patches import cv2_imshow
import math
#Black Pixels
def findBlacks(final,x1,x2,y1,y2):
  bpixels = 0;
  for x in range(x1, x2-1):
    for y in range(y1, y2-1):
      curr = final[y,x]
      if curr == 0:
        bpixels+=1
  return bpixels

# Find Normal Size
def findNormSize(left,right,top,bottom,bpix):
  if bpix != 0:
    return (((right-left)*(bottom-top))/bpix)
  else:
    return ((right-left)*(bottom-top))

# Find Centroids Angle
def findCentralAngle(cx,cy,bottom,left):
  dx = cx - left
  dy = bottom - cy
  if(dx == 0):
    dx = 1
  return math.atan(dy/dx)

# Find Normalised Angles of Black Pixels
def findNormAngles(image,x1,x2,y1,y2):
  bpixels = 0
  A = 0
  for x in range(x1, x2-1):
    for y in range(y1, y2-1):
      curr = image[y,x]
      if curr == 0:
        bpixels +=1
        dx = x - x1
        dy =  y2 - y
        if(dx == 0):
          dx = 1
        A+=math.atan(dy/dx)
  if bpixels == 0:
    bpixels = 1
  return A/bpixels

#transition fuction
def transition(x1,x2,y1,y2,final):  
  prev = final[y1,x1]
  n = 0
  for x in range(x1, x2-1):
    for y in range(y1, y2-1):
      curr = final[y,x]
      if curr == 255 and prev == 0: #count every white pixel after balck pixel
        n = n + 1
      prev = curr
  return n

#ratio function
def findRatio(left,  right,  top,  bottom):
  return ((right-left)/(bottom-top)) #ratio=width/height

#Centroid function
def findCentroid2(image,  left,  right,  top,  bottom):
  cx = left
  cy = top
  n = 0

  for x in range(left,right-1):
    for y in range(top, bottom-1):
      if cropImg[y,x] == 0:
        cx = cx + x
        cy = cy + y
        n = n + 1
  if n !=0:  #if section isnt empty
    cx = cx/n
    cy = cy/n

  return int(cx), int(cy)

#Centroid function
def findCentroid(image,  left,  right,  top,  bottom):
  cx = left
  cy = top
  n = 0

  for x in range(left,right-1):
    for y in range(top, bottom-1):
      if cropImg[y,x] == 0:
        cx = cx + x
        cy = cy + y
        n = n + 1
  if n !=0:  #if section isnt empty
    cx = cx/n
    cy = cy/n
   
  #write centroid to text file
  f= open("centroid.txt","a+")
  f.write("%f , %f \n" % (cy , cx))
  f.close()

  print("Centroid Value:",cy,cx)
 
  cImg = cropImg
  for x in range(left,right-1):
    for y in range(top, bottom-1):
      cImg[int(cy),x] = 50  #print boundaries
      cImg[y,int(cx)] = 50
   
  cv2_imshow(cImg)
  return int(cx), int(cy)

#split function
def split(image,left,right,top,bottom, depth =0): 
  if  depth  <  3:
    cx,  cy  =  findCentroid(image,  left,  right,  top,  bottom)
    if cx != 0 and cy != 0:
      split(image,  left,  cx,  top,  cy,  depth  +  1)  #called recursively for four sectors around each centroid
      split(image,  cx,  right,  top,  cy,  depth  +  1) 
      split(image,  left,  cx,  cy,  bottom,  depth  +  1) 
      split(image,  cx,  right,  cy,  bottom,  depth  +  1)
  else:  #if sector cant be divided further
    cx,  cy  =  findCentroid2(image,  left,  right,  top,  bottom)
    t  =  transition(left,  right,  top,  bottom,image) 
    r  =  findRatio(left,  right,  top,  bottom)

    bpix = findBlacks(image, left, right, top, bottom)
    s = findNormSize(left,right,top,bottom,bpix)
    a = findCentralAngle(cx,cy,bottom,left)
    A = findNormAngles(image,left,right,top,bottom)
    
    print("Centroid: ", cy ," ", cx )
    print("Black Pixels: ", bpix)
    print("Normalised Size: ", s)
    print("Inclination of Centroid: ", a)
    print("Normalised Inclination of black pixels: ", A)
    print("transitions: ", t)
    print("Aspect ratio ", r, "\n")

    #write transitions to text file
    f1= open("transitions.txt","a+")
    f1.write("%f\n" % t)
    f1.close()

    #write aspect ratio to text file
    f2= open("aspectRatio.txt","a+")
    f2.write("%f\n" % r)
    f2.close()

    #write centroids to text file
    f1= open("centroid2.txt","a+")
    f1.write("%f , %f\n" % (cy,cx))
    f1.close()

    #write Black Pixels in a cell to text file
    f1= open("blackpixels.txt","a+")
    f1.write("%f\n" % bpix)
    f1.close()

    #write Normalised Size to text file
    f1= open("NormalisedSize.txt","a+")
    f1.write("%f\n" % s)
    f1.close()

    #write Inclination of Centroids to text file
    f1= open("IncOfCen.txt","a+")
    f1.write("%f\n" % a)
    f1.close()

    #write Normalised Inclination of Black Pixels to text file
    f1= open("NormIncofBlackPixels.txt","a+")
    f1.write("%f\n" % A)
    f1.close()

#main 
img = cv2.imread('123.jpg',0) #read image
(thresh, bWImg) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY) #conert to binary
print("Black and White Image:")
cv2_imshow(bWImg)
hei,wid = bWImg.shape #find height and width of image
left = wid 
right = 0 
top = hei 
bottom = 0

#crop image
for x in range(0,wid-1):
  for y in range(0, hei-1):
    color = bWImg[y,x]
    if color==0:
      if x > right:
        right = x
      if x < left:
        left = x
      if y > bottom:
        bottom = y
      if y < top:
        top = y

cropImg = bWImg[top:bottom, left:right]

print("Cropped Image:")
cv2_imshow(cropImg)
cImg = cropImg
for x in range(0,right-left-1): #assign bounding box to cropped image
  for y in range(0, bottom-top-1):
    cImg[0,x] = 50
    cImg[y,0] = 50
    cImg[bottom-top-1,x] = 50
    cImg[y,right-left-1] = 50

#split image
split(cropImg,0,right-left,0,bottom-top)