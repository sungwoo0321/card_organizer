import cv2
import time

# 웹캠 열기
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

orb = cv2.ORB_create()

while True:
    # 현재 시간 측정
    start_time = time.time()

    # 웹캠에서 프레임 읽기
    ret, frame = cap.read()

    # 읽기에 걸린 시간 측정
    read_time = (time.time() - start_time) * 1000

    print(f"Read time: {read_time} ms")

    kp, des = orb.detectAndCompute(frame, None)
    orb_time = (time.time() - start_time) * 1000

    print(f"ORB time: {orb_time} ms")


    # 'q' 키를 누르면 루프 종료
    cv2.imwrite('frame.png', frame)
    time.sleep(1)


# 웹캠 닫기
cap.release()