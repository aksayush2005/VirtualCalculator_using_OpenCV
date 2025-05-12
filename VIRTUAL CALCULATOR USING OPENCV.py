import cv2
import mediapipe as mp
import time
cap=cv2.VideoCapture(0)
cap.set(3,1400)
cap.set(4,800)
def calculator_UI(frame,button_list):
    frame_height,frame_width=frame.shape[:2]
    for button in button_list:
        x,y=button.pos
        w,h=button.size
        cv2.rectangle(frame,(100*y+25,100*x+25),(100*y+w+25,100*x+h+25),(0,255,255),2)
        cv2.putText(frame,str(button.value),(100*y+70,100*x+70),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),2)
        if results.right_hand_landmarks:
            index_finger_tip=results.right_hand_landmarks.landmark[8]
            index_finger_tip_x=index_finger_tip.x
            index_finger_tip_y=index_finger_tip.y
            if 100*y+25<index_finger_tip_x*frame_width<100*y+w+25 and 100*x+25 <index_finger_tip_y*frame_height<100*x+h+25:
                cv2.rectangle(frame,(100*y+25,100*x+25),(100*y+w+25,100*x+h+25),(0,0,255),2)
                cv2.putText(frame, str(button.value), (100 * y + 70, 100 * x + 70), cv2.FONT_HERSHEY_PLAIN, 4,(0,0, 255), 2)


class Buttons:
    def __init__(self,pos,value,size=(100,100)):
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
    if results.right_hand_landmarks:
        right_list=results.right_hand_landmarks.landmark
        x=right_list[8].x
        cv2.putText(frame,f'{x}',(60,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    calculator_UI(frame,button_list)
    cv2.imshow("Video",frame)
    if cv2.waitKey(1) & 0xFF==ord("q"):
       break
cap.release()
cv2.destroyAllWindows()
