import cv2
import cvzone
import numpy as np
import pickle

cap = cv2.VideoCapture('carPark.mp4')
with open('CarParkPos','rb') as f:
    poslist = pickle.load(f)

width, height = 107, 48
def process(imgpro):
    parkingspace_count = 0
    for pos in poslist:
        x,y = pos
        imgcrop = imgpro[y:y+height,x:x+width]
        count = cv2.countNonZero(imgcrop)


        if count<900:
            color = (0,255,0)
            thickness = 4
            parkingspace_count+=1
        else:
            color = (0,0,255)
            thickness = 3

        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height),color,thickness)
        cvzone.putTextRect(img,str(count),(x,y+height-3),scale=1,colorR=color,thickness=4,offset=0)
    
    cvzone.putTextRect(img,f"empty:{parkingspace_count}/{len(poslist)}",(100,50),scale=5,colorR = (0,255,0),thickness = 4,offset=20)        

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    ret,img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgthreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16 )
    imgmedian = cv2.medianBlur(imgthreshold,5)
    kernel = np.ones((3,3))
    imgdilate = cv2.dilate(imgmedian,kernel)


    process(imgdilate)
    cv2.imshow("ImageBlur", img)
    cv2.waitKey(10)
    

   