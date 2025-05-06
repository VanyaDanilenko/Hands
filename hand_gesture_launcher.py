import cv2
import mediapipe as mp
import subprocess
import time
import os
import sys


# Ініціалізація MediaPipe 
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Запуск камери
cap = cv2.VideoCapture(0)

# Перевірка, чи вже запущена програма 
dota2_process = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Перетворення зображення для обробки
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Обробка кількості пальців
    finger_count = 0
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            
            if landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y:
                finger_count += 1

            for i in [1, 2, 3, 4]:  
                if landmarks.landmark[mp_hands.HandLandmark(i * 4 + 3)].y < landmarks.landmark[mp_hands.HandLandmark(i * 4 + 2)].y:
                    finger_count += 1

        
        cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Логіка запуску програми
    if finger_count == 2 and dota2_process is None:
        print("2 пальці - Запускаю Dota 2")
        dota2_process = subprocess.Popen([r"F:\SteamLibrary\steamapps\common\dota 2 beta\\game\\bin\\win64\\dota2.exe"])
        break  

    elif finger_count == 4 and dota2_process is None:
        print("4 пальці - Запускаю калькулятор Windows")
        subprocess.Popen("calc") 
        break  

    
    elif finger_count == 1 or finger_count == 3 or finger_count == 5:
        pass

   
    cv2.imshow("Hand Gesture Control", frame)

    
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        print("Програма завершена.")
        break


cap.release()
cv2.destroyAllWindows()


sys.exit()
