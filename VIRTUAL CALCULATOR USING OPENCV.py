import cv2
import mediapipe as mp
import time
import pyttsx3
import threading
import numpy as np
import copy
engine = pyttsx3.init()
cap=cv2.VideoCapture(0)
cap.set(3,1400)
cap.set(4,800)
x0,y0=0,0
mask=np.zeros((720,1280,3),np.uint8)
flag=0
def calculator_UI(frame,button_list):
    cv2.line(frame,(700,0),(700,700),(255,255,255),2)
    frame_height,frame_width=frame.shape[:2]
    global result
    global x0,y0
    global flag
    for button in button_list:
        x,y=button.pos
        w,h=button.size
        cv2.rectangle(frame,(100*y+65,100*x+65),(100*y+w+65,100*x+h+65),(50,50,50),-1)
        cv2.putText(frame,str(button.value),(100*y+110,100*x+110),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),2)
        if results.right_hand_landmarks:

            right_index_tip=results.right_hand_landmarks.landmark[8]
            right_index_tip_x=right_index_tip.x
            right_index_tip_y=right_index_tip.y
            right_thumb_tip=results.right_hand_landmarks.landmark[4]
            right_thumb_tip_x=right_thumb_tip.x
            right_thumb_tip_y=right_thumb_tip.y
            distance_right= ((((right_index_tip_x - right_thumb_tip_x) * frame_width) ** 2 + ((right_index_tip_y - right_thumb_tip_y) * frame_height) ** 2) )**0.5
            if 100*y+65<right_index_tip_x*frame_width<100*y+w+65 and 100*x+65 <right_index_tip_y*frame_height<100*x+h+65:
                cv2.rectangle(frame,(100*y+65,100*x+65),(100*y+w+65,100*x+h+65),(220,205,105),-1)
                cv2.putText(frame, str(button.value), (100 * y + 110, 100 * x + 110), cv2.FONT_HERSHEY_PLAIN, 4,(0,0,0), 2)
                time.sleep(0.25)
                if distance_right<50:
                        cv2.rectangle(frame, (100 * y + 65, 100 * x + 65), (100 * y + w + 65, 100 * x + h + 65),(114,88, 2), -1)
                        #cv2.putText(frame,str(distance),(60,60),cv2.FONT_HERSHEY_PLAIN,4,(255,255,0),2)
                        cv2.putText(frame, str(button.value), (100 * y + 110, 100 * x + 110), cv2.FONT_HERSHEY_PLAIN, 4,(255,255,255), 2)
                        #cv2.line(frame,(right_thumb_tip_x*frame_width,right_thumb_tip_y*frame_height),(right_thumb_tip_x*frame_width,right_thumb_tip_y*frame_height),(255,0,255),2)
                        result=calculator(button.value)


            if 700<right_index_tip_x*frame_width<frame_width and 0<right_index_tip_y*frame_height<700:

                right_index_tip=results.right_hand_landmarks.landmark[8]
                right_index_tip_x=right_index_tip.x
                right_index_tip_y=right_index_tip.y
                right_thumb_tip=results.right_hand_landmarks.landmark[4]
                right_thumb_tip_x=right_thumb_tip.x
                right_thumb_tip_y=right_thumb_tip.y
                distance_right= ((((right_index_tip_x - right_thumb_tip_x) * frame_width) ** 2 + ((right_index_tip_y - right_thumb_tip_y) * frame_height) ** 2) )**0.5
                if distance_right<25:
                    if flag==1:
                        x0,y0=0,0
                        flag=0

                    xp, yp = (right_index_tip.x) * frame_width, (right_index_tip.y) * frame_height
                    if (x0,y0)==(0,0):
                        x0,y0=xp,yp

                    cv2.line(mask,(int(x0),int(y0)),(int(xp),int(yp)),(255,255,255),2)
                    x0,y0=xp,yp




                    #print(xp,yp)

                    #for i in drawing_list:
                        #cv2.circle(frame,i,100,(255,255,255),2)
        cv2.putText(frame, str(result), (200,620), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)




def speak(text):
    engine.say(text)
    engine.runAndWait()
result= ''
exp_list=[]
def calculator(value):
    global mask
    exp=''
    global flag
    try:
        if value != '=' and value != 'C' and value != 'CAP' and value != 'E':
            exp_list.append(value)
            if value=='-':
                threading.Thread(target=speak,args=("minus",)).start()
            elif value=='*':
                threading.Thread(target=speak, args=("multiplied by",)).start()
            elif value=="/":
                threading.Thread(target=speak, args=("divided by",)).start()

            else:
                threading.Thread(target=speak, args=(value,)).start()

            return "".join(str(i) for i  in exp_list)
        elif value=='E' or value=='CAP':
            if value == 'E':
                flag=1
                mask=np.zeros((720,1280,3),np.uint8)
                return "".join(str(i) for i  in exp_list)


        else:

            if value == '=':

                for i in exp_list:
                    exp=exp+str(i)

                exp=eval(exp)

                threading.Thread(target=speak,args=("equals",)).start()

                return exp
            elif value == 'C':
                exp_list.clear()
                threading.Thread(target=speak,args=("Clear",)).start()
                return ""
    except:
        threading.Thread(target=speak,args=("Invalid Input",)).start()
        return "Invalid input"






class Buttons:
    def __init__(self,pos,value,size=(90,90)):
        self.pos=pos
        self.value=value
        self.size=size
buttons=[[7,8,9,'+'],
         [4,5,6,'-'],
         [1,2,3,'/'],
         ['=',0,"C",'*'],
         ['P','','','E']]
button_list=[]
for i in range(0,len(buttons)):
    for j,value in enumerate(buttons[i]):
        button_list.append(Buttons((i,j),value))




mp_drawing=mp.solutions.drawing_utils
mp_holistic=mp.solutions.holistic
with mp_holistic.Holistic(min_detection_confidence=0.7,min_tracking_confidence=0.7) as holistic:

  while cap.isOpened():

    ret,frame=cap.read()
    frame = cv2.flip(frame, 1)

    image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=holistic.process(image)
    image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(frame,results.face_landmarks,mp_holistic.FACEMESH_TESSELATION,
                              mp_drawing.DrawingSpec(color=[255,0,0],thickness=1,circle_radius=1),
                              mp_drawing.DrawingSpec(color=[255,0,0],thickness=1,circle_radius=1))
    #mp_drawing.draw_landmarks(frame,results.right_hand_landmarks,mp_holistic.HAND_CONNECTIONS)
    #mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    #mp_drawing.draw_landmarks(frame,results.pose_landmarks,mp_holistic.POSE_CONNECTIONS)
    '''if results.right_hand_landmarks:
        right_list=results.right_hand_landmarks.landmark
        x=right_list[8].x
        cv2.putText(frame,f'{x}',(60,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)'''
    calculator_UI(frame,button_list)
    frame=cv2.addWeighted(mask,1,frame,1,0)
    cv2.imshow('drawingboard',mask)
    cv2.imshow("Video",frame)
    if cv2.waitKey(1) & 0xFF==ord("q"):
       break
engine.stop()
cap.release()
cv2.destroyAllWindows()
