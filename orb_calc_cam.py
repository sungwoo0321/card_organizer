import cv2
from enum import Enum
import time 

class CardType(Enum):
    BACK = 0
    FRONT = 1
    BOTTOM = 2

orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

back_match_threshold = 10
bottom_match_threshold = 10

back_img = None
back_kp = None
bottom_des = None

def orb_classifier(img):
    global back_des, bottom_des

    kp, current_des = orb.detectAndCompute(img, None)

    if back_des is None:
        back_des = current_des
        return CardType.BACK
    
    back_matches = bf.match(back_des, current_des)
    back_matches = sorted(back_matches, key=lambda x: x.distance)

    match_threshold = 30
    good_back_matches = [m for m in back_matches if m.distance < match_threshold]
    print(f"good_back_matches: {len(good_back_matches)}")
    if len(good_back_matches) > back_match_threshold:
        return CardType.BACK
    
    # if bf.match(bottom_des, current_des) > bottom_match_threshold:
    #     return CardType.BOTTOM
    
    return CardType.FRONT


cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))


back_des = None
bottom_des = None

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

# 영상을 캡처하고 화면에 표시합니다.
while True:
    user_input = input("Please enter something: ")

    ret, frame = cap.read()
    frame = frame[0:290, 0:640]

    if back_des is None:
        back_img = frame
        cv2.imwrite(f'temp/back.jpg', frame)

        back_kp, back_des = orb.detectAndCompute(frame, None)
        print("back_des is set")
        continue


    # 현재 시간을 파일 이름으로 저장
    cv2.imwrite(f'temp/{time.time()}.jpg', frame)

    if not ret:
        print("프레임을 캡처할 수 없습니다.")
        break

    # 프레임을 화면에 표시합니다.
    # cv2.imshow('frame', frame)

    _, current_des = orb.detectAndCompute(frame, None)

    ret = orb_classifier(frame)

    print(ret)

# 작업이 끝나면 해제합니다.
cap.release()
cv2.destroyAllWindows()