from pynput.keyboard import Key, Listener
import numpy as np
import cv2
import mss
import mss.tools
import time
import socket


def on_press(key):
    #print('{0} pressed'.format(key))
    if key == Key.alt_l:
        #print("alt pressed")
        with mss.mss() as sct:
            # The screen part to capture
            monitor = {"top": 400, "left": 705, "width": 250, "height": 250}
            output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

            # Grab the data
            sct_img = sct.grab(monitor)

            # Save to the picture file
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

            image = cv2.imread('sct-400x705_250x250.png')
            result = image.copy()
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            #lower = np.array([114,14,0])
            #upper = np.array([179,145,255])
            
            lower = np.array([148,69,0])
            upper = np.array([179,132,255])

            #lower = np.array([179,0,0])
            #upper = np.array([179,115,255])
            
            mask = cv2.inRange(image, lower, upper)
            
            kernel = np.ones((3,3), np.uint8)
            dilated = cv2.dilate(mask, kernel, iterations=5)
            
            contours, hierarchy = cv2.findContours(dilated,  
                cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            try:
                cluster = {}
                for dot in contours:
                    x,y,w,h = cv2.boundingRect(dot)
                    dist = ((135-(x+(w//2)))**2+(124-(y+(h//2)))**2)

                    if bot_mode == 0:
                        if dist < 10600:
                            #cv2.circle(image, ((x+(w//2)),(y+(h//2))) , 4, (127,127,0), -1, 8)
                            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
                            if op_mode == 0:
                                cluster[h*w] = (x+(w//2), y+(h//8)+5)
                            else:
                                cluster[h*w] = (x+(w//2), y+(h//4)+5)
                            
                    else:
                        if dist < 10600:
                            if op_mode == 0:
                                cluster[y] = (x+(w//2), y+(h//4)+5)
                            else:
                                cluster[y] = (x+(w//2), y+(h//2)+5)
                            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
                            
                if bot_mode == 0:            
                    head = cluster[max(cluster)]
                    cv2.circle(image, head, 5, (127,127,0), -1, 8)
                else:
                    head = cluster[min(cluster)]
                    cv2.circle(image, (head), 5, (127,127,0), -1, 8)
                    
                #print("head: "+str(head))
                coordx = (head[0]-135)//0.584
                coordy = (head[1]-124)//0.584
                #print(coordx, coordy)
                int(coordx)
                if coordx > -80 and coordx < 0:
                    coordx -= 6
                elif coordx < 80 and coordx > 0:
                    coordx += 6
                elif coordx < -80:
                    coordx -= 15
                elif coordx > 80:
                    coordx += 15

                    
                if coordy > -80 and coordy < 0:
                    coordy -= 6
                elif coordy < 90 and coordy > 0:
                    coordy += 8
                elif coordy < -80:
                    coordy -= 15
                elif coordy > 80:
                    coordy += 19
                if coordx < 128 and coordy < 128 and coordx > -128 and coordy > -128:
                    coords = (coordx, coordy)
                    coordx = int(coordx)
                    coordy = int(coordy)
                    print(coordx, coordy)
                    msgFromClient       = str(coordx)+" "+str(coordy)
                    bytesToSend         = str.encode(msgFromClient)
                    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
                else:
                    pass
                    #print("Mouse value out of range")


            except:
                pass


            cv2.imshow('Penis', image)
            cv2.waitKey(1) 

def on_release(key):
    pass

bot_mode = 0
op_mode = 0

serverAddressPort   = ("192.168.1.191", 20001)
bufferSize          = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
