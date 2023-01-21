from glob import glob
import cv2
import imutils
import numpy as np
import imutils
import pytesseract
from pytesseract import Output

files = glob('./docImages/aadhar/*')
# print(files)
for i in files:
    img = cv2.imread(i)
    temp = img.copy()
    temp_state = []
    total_quit = False
    while (True):
        cv2.imshow("Preview", temp)
        key = cv2.waitKey(0)
        # Gray (g)
        if key == ord("g") and "g" not in temp_state:
            temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
            temp_state.append("g")
        
        # Blur (b)
        if key == ord("b"):
            temp = cv2.medianBlur(temp, 9)
        
        # Threshold (t)
        if key == ord("t"):
            temp = cv2.adaptiveThreshold(temp, 255, 
                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
            temp_state.append("t")
        
        # Edges (e)
        if key == ord("e") and "t" not in temp_state and "g" in temp_state:
            edged = cv2.Canny(temp, 50, 150)
            backtorgb = cv2.cvtColor(temp,cv2.COLOR_GRAY2RGB)
            cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            initiated = True
            max_area_cnt = []
            max_area = None
            for i in cnts:
                x, y, w, h = cv2.boundingRect(i)
                cv2.rectangle(backtorgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow("backtorgb", backtorgb)
            cv2.waitKey(0)
#             cropped = False
#             while(True):
#                 cv2.imshow("backtorgb", backtorgb)
#                 key2 = cv2.waitKey(0)
#                 if key2 == ord("p") and not cropped:
#                     c = max(cnts, key = cv2.contourArea)
#                     x,y,w,h = cv2.boundingRect(c)
#                     cv2.rectangle(backtorgb,(x,y),(x+w,y+h),(0,255,0), 2)
#                     cropped = True
#                 if key2 == ord("q"):
#                     break
            
            cv2.destroyAllWindows()
            
        
        # Big (r)
        if key == ord("r"):
            temp = cv2.resize(temp, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
            
        # Small (r)
        if key == ord("y"):
            temp = cv2.resize(temp, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        
        # Reset (s)
        if key == ord("s"):
            temp = img.copy()
            temp_state = []
        
        # Sharpening (z)
        if key == ord("z"):
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            temp = cv2.filter2D(temp, -1, kernel)
        
        #Erosion: (k)
        if key == ord("k") and "g" in temp_state:
            temp = cv2.erode(temp.copy(), None, 1)
        
        #Dilation (j)
        if key == ord("j") and "g" in temp_state:
            temp = cv2.dilate(temp.copy(), None, 1)
            
        #Opening (o)
        if key == ord("o") and "g" in temp_state:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            temp = cv2.morphologyEx(temp, cv2.MORPH_OPEN, kernel)
        
        #Closing (p)
        if key == ord("o") and "g" in temp_state:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            temp = cv2.morphologyEx(temp, cv2.MORPH_OPEN, kernel)
        
        #Lines (l)
        if key == ord("l") and "t" not in temp_state and "g" in temp_state:
            edged = cv2.Canny(temp, 50, 150)
            lines = cv2.HoughLinesP(edged, 1, np.pi/180, 200)
            backtorgb = cv2.cvtColor(temp,cv2.COLOR_GRAY2RGB)
            for line in lines:
                x1, y1, x2, y2 = line[0]
                print(x1, y1, x2, y2)
        
        if key == ord("i") and "t" not in temp_state and "g" in temp_state:
            rgb = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)
            config  = ('-l eng --oem 3 --psm '+ str(11))
            
            try:
                text = pytesseract.image_to_string(rgb, lang='eng', config=config)
            except Exception as e:
                print("Fuck you ",e)
                continue
            
            try:
                results = pytesseract.image_to_osd(rgb, config='--psm 0 -c min_characters_to_try=4', output_type=Output.DICT)
            except Exception as e:
                print("Fuck you ",e)
                continue
            
            # display the orientation information
            print("[INFO] detected orientation: {}".format(
                results["orientation"]))
            print("[INFO] rotate by {} degrees to correct".format(
                results["rotate"]))
            print("[INFO] detected script: {}".format(results["script"]))
            
            
        # Quit (q)
        if key == ord("q"):
            break
            
        # Total Quit (/)
        if key == ord("/"):
            total_quit = True
            break
        
    
    if total_quit:
        break
cv2.destroyAllWindows()

