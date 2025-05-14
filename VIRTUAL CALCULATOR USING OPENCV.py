import cv2
import mediapipe as mp
import time
cap=cv2.VideoCapture(0)
cap.set(3,1400)
cap.set(4,800)
def calculator_UI(frame,button_list):
    frame_height,frame_width=frame.shape[:2]
    global result
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

                    result=calculator(button.value)
        cv2.putText(frame,str(result),(700,160),cv2.FONT_HERSHEY_PLAIN,4,(0,0,0),4)

result= ''
exp_list=[]
def calculator(value):
    exp=''
    try:
        if value != '=' and value != 'C':
            exp_list.append(value)

            return "".join(str(i) for i  in exp_list)

        else:

            if value == '=':
                for i in exp_list:
                    exp=exp+str(i)

                exp=eval(exp)

                return exp
            elif value == 'C':
                exp_list.clear()
                return ""
    except:
        return "Invalid input"






class Buttons:
    def __init__(self,pos,value,size=(90,90)):
        self.pos=pos
        self.value=value
        self.size=size
buttons=[[7,8,9,'+'],
         [4,5,6,'-'],
         [1,2,3,'/'],
         ['=',0,"C",'*']]
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
    mp_drawing.draw_landmarks(frame,results.right_hand_landmarks,mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(frame,results.pose_landmarks,mp_holistic.POSE_CONNECTIONS)
    '''if results.right_hand_landmarks:
        right_list=results.right_hand_landmarks.landmark
        x=right_list[8].x
        cv2.putText(frame,f'{x}',(60,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)'''
    calculator_UI(frame,button_list)

    cv2.imshow("Video",frame)
    if cv2.waitKey(1) & 0xFF==ord("q"):
       break
cap.release()
cv2.destroyAllWindows()
