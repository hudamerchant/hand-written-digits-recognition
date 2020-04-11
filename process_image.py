import cv2
import numpy as np        
import matplotlib.pyplot as plt
from scipy import ndimage
import math
from keras.models import load_model


# loading trained model
model = load_model('trained_model.h5')

def predict_digit(img):
    test_image = img.reshape(-1,28,28,1)
    return np.argmax(model.predict(test_image))


#putting label
def put_label(digit,label,x,y):
    font = cv2.FONT_HERSHEY_SIMPLEX
    label_x = int(x) - 10
    label_y = int(y) + 10
    cv2.rectangle(digit,(label_x,label_y+5),(label_x+35,label_y-35),(0,255,0),-1) 
    cv2.putText(digit,str(label),(label_x,label_y), font,1.5,(255,0,0),1,cv2.LINE_AA)
    return digit

# refining each digit
def digit_refiner(gray):
    org_size = 22
    img_size = 28
    rows,cols = gray.shape
    
    if rows > cols:
        factor = org_size/rows
        rows = org_size
        cols = int(round(cols*factor))        
    else:
        factor = org_size/cols
        cols = org_size
        rows = int(round(rows*factor))
    gray = cv2.resize(gray, (cols, rows))
    
    #get padding 
    colsPadding = (int(math.ceil((img_size-cols)/2.0)),int(math.floor((img_size-cols)/2.0)))
    rowsPadding = (int(math.ceil((img_size-rows)/2.0)),int(math.floor((img_size-rows)/2.0)))
    
    #apply padding 
    gray = np.lib.pad(gray,(rowsPadding,colsPadding),'constant')
    return gray


def process(path):
  
    img = cv2.imread(path,2)
    img_org =  cv2.imread(path)

    ret,thresh = cv2.threshold(img,127,255,0)
    im2,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    for j,cnt in enumerate(contours):
        epsilon = 0.01*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        
        hull = cv2.convexHull(cnt)
        k = cv2.isContourConvex(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        
        if(hierarchy[0][j][3]!=-1 and w>10 and h>10):
            #putting boundary on each digit
            cv2.rectangle(img_org,(x,y),(x+w,y+h),(0,255,0),2)
            
            #cropping each image and process
            cropped_img = img[y:y+h, x:x+w]
            cropped_img = cv2.bitwise_not(cropped_img)
            cropped_img = digit_refiner(cropped_img)
            th,fnl = cv2.threshold(cropped_img,127,255,cv2.THRESH_BINARY)

            # getting prediction of cropped image
            pred = predict_digit(cropped_img)

            # placing label on each digit
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            img_org = put_label(img_org,pred,x,y)

    return img_org