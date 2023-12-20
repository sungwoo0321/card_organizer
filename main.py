from enum import Enum
import serial
import cv2

class CardOrganzier:
    class CardType(Enum):
        BACK = 0
        FRONT = 1
        BOTTOM = 2

    def __init__(self):
        # Set Camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Set ORB
        self.orb = cv2.ORB_create()
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # Set threshold
        self.back_match_threshold = 10
        self.bottom_match_threshold = 10

        # Init descriptors
        self.back_des = None
        self.bottom_des = None  # TODO

        # Set Serial
        # 시리얼 포트 설정 (예: Windows의 경우 'COM3', Linux/macOS의 경우 '/dev/ttyUSB0' 등으로 될 수 있음)
        # 시리얼 포트 이름은 시스템 실제 해당하는 것으로 변경
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        # self.ser = serial.Serial('/dev/cu.usbmodem1101', 9600, timeout=1)
        self.wait_for_arduino()

    def wait_for_arduino(self):
        print("waiting for Arduino to be ready...")
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode().strip()
                print(f"Received from Arduino: {line}")
                if line == "READY":
                    break
        print("Arduino is ready!")

    def orb_classifier(self, img):
        _, current_des = self.orb.detectAndCompute(img, None)

        if self.back_des is None:
            self.back_des = current_des
            return self.CardType.BACK

        # Compare with back_des
        back_matches = self.bf.match(self.back_des, current_des)
        back_matches = sorted(back_matches, key=lambda x: x.distance)

        match_threshold = 30
        good_back_matches = [
            m for m in back_matches if m.distance < match_threshold]

        if len(good_back_matches) > self.back_match_threshold:
            return self.CardType.BACK

        # Compare with bottom_des
        bottom_matches = self.bf.match(self.bottom_des, current_des)
        bottom_matches = sorted(bottom_matches, key=lambda x: x.distance)

        if len(bottom_matches) > self.bottom_match_threshold:
            return self.CardType.BOTTOM

        # If not back or bottom, it is front
        return self.CardType.FRONT
    
    def calc_angle(self, ret):
        print(ret.name)
        if ret == self.CardType.BACK:
            return "1"
        elif ret == self.CardType.FRONT:
            return "2"
        else:
            return "3"

    def run(self):
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode().strip()
                print(f"Received from Arduino: {line}")

                if line.startswith("request"):
                    _, frame = self.cap.read()
                    ret = self.orb_classifier(frame)

                    if ret == self.CardType.BOTTOM:
                        self.ser.write("FINISH\n".encode('utf-8'))
                        print("Organizing cards is done!")

                    angle = self.calc_angle(ret)
                    self.ser.write((angle + "\n").encode('utf-8'))
                    print(f"Sent to Arduino: {angle}")

if __name__ == "__main__":
    organizer = CardOrganzier()
    organizer.run()