enum CardType {
    BACK,
    FRONT,
    BOTTOM
};

CardType stringToCardType(String str) {
    if (str == "BACK") return BACK;
    else if (str == "FRONT") return FRONT;
    else if (str == "BOTTOM") return BOTTOM;
}

void setup() {
  // 시리얼 통신 시작
  Serial.begin(9600);
  while (!Serial) {
    ; // USB 연결이 될 때까지 기다립니다.
  }
  Serial.println("READY");
}

// TODO
void rotate(int angle) {
  Serial.print("rotate ");
  Serial.println(angle);
}

// TODO
void drawCard() {
  Serial.println("draw ");
}

CardType request() {
    Serial.println("request");
    while(!Serial.available()) {
        delay(100);
    }
    String result = Serial.readStringUntil('\n');
    return stringToCardType(result);
}

// TODO
int calcAngle(CardType type) {
    switch(type) {
        case BACK:
            return 0;
        case FRONT:
            return 180;
        case BOTTOM:
            return 90;
    }
}

void loop() {
    while(true) {
        CardType type = request();
        if(type == BOTTOM) {
            break;
        }
        int angle = calcAngle(type);
        rotate(angle);
        drawCard();
    }

    Serial.println("END");
}