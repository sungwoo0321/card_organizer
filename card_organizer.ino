#include <Servo.h>

Servo main_servo;

// TODO
void rotate(int angle) {
  Serial.println("rotate");
}

// TODO
void drawCard() {
  Serial.println("draw");
}

void setup() {
    // 서보 모터 연결
    int const SERVO_PIN = 2;
    main_servo.attach(SERVO_PIN);

    // 시리얼 통신 시작
    Serial.begin(9600);
    while (!Serial) {
        ; // USB 연결이 될 때까지 기다립니다.
    }
    Serial.println("READY");
}

void loop() {
    while(true) {
        Serial.println("request");
        while(!Serial.available()) {
            delay(100);
        }

        String message = Serial.readStringUntil('\n');
        if(message == "FINISH"){
          break;
        }

        int angle = message.toInt();
        rotate(angle);

        drawCard();
    }

    Serial.println("END");
}