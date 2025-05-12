import cv2
import mediapipe as mp

cap=cv2.VideoCapture(0)
cap.set(3,500)
cap.set(4,740)
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

    cv2.imshow("Video",frame)
    if cv2.waitKey(1) & 0xFF==ord("q"):
       break
cap.release()
cv2.destroyAllWindows()
