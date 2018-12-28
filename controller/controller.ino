#include <MFRC522.h>

#include <SPI.h>
#include <Wire.h>

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#include <ArduinoJson.h>


#define RST_PIN  0
#define SS_PIN  15

#define OLED_RESET 2

#define DUMMY_TIMER 100

#define HEAD "TEST CONFERENCE"
#define SECTION_ID 1
#define SECTION_NAME "Astrophysics" 

#define HOST_ADDR "10.0.0.1"
#define HOST_PORT 8080

#define WIFI_SSID "Pi3-AP"
#define WIFI_PSWD "9hyV1Xe8"


MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;
struct attendee {
    uint16_t id;
    char sname[17];
	  char fname[17];
};

Adafruit_SSD1306 display(OLED_RESET);


void setup() {
    Serial.begin(115200);
    Serial.println();
    SPI.begin();
    display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(WHITE);
    mfrc522.PCD_Init();
    for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;
    wifi_connect();
    oled_write_line(SECTION_NAME, "");
    delay(1500);
}

void loop() {
    static unsigned int dummy_timer = DUMMY_TIMER;

    if (!dummy_timer)
        oled_write_line("Attach your card", "");
    if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
        delay(50);
        if (dummy_timer) dummy_timer--;
        return;
    }
    dummy_timer = DUMMY_TIMER;
    attendee att;
    rfid_read_tag(&att);
    print_attendee(&att);
    oled_write_line(String(att.sname), String(att.fname));
    send_data(&att);
}

void send_data(attendee *att) {
    StaticJsonDocument<255> json_buff;
    JsonObject main_json = json_buff.to<JsonObject>();
    JsonObject att_json = main_json.createNestedObject("attendee");
    JsonObject sect_json = main_json.createNestedObject("section");
    att_json["id"] = att->id;
    att_json["name"] = att->sname;
    att_json["surname"] = att->fname;
    sect_json["id"] = SECTION_ID;
    sect_json["name"] = SECTION_NAME;
    char json_str[255];
    serializeJsonPretty(main_json, json_str, sizeof(json_str));

    HTTPClient http;
    http.begin("http://" + String(HOST_ADDR) + ":" + String(HOST_PORT) + "/sections/" + String(SECTION_ID) + "/track");
    http.addHeader("Content-Type", "application/json");
    if (!~http.sendRequest("PUT", json_str)) {
        oled_write_line("CONNECTION ERROR", "");
        delay(1000);
    }
    http.end();
}

void wifi_connect() {
    oled_write_line("Connecting to Wi-Fi", "");
    WiFi.begin(WIFI_SSID, WIFI_PSWD);
    while (WiFi.status() != WL_CONNECTED) delay(500);
    oled_write_line("Connection done!", "");
    delay(1000);
    oled_write_line("IP: " + WiFi.localIP().toString(), "");
    delay(1500);
}

void oled_write_line(String name, String fname) {
    display.clearDisplay();
    display.setCursor(0,0);
    display.print(HEAD);
    display.setCursor(0,10);
    display.println(name);
    display.println(fname);
    display.display();
}

void rfid_read_tag(attendee *att) {
    MFRC522::StatusCode status;
    byte len = 18;
    byte blk_buf[len];

    status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, 4, &key, &(mfrc522.uid));
    if (status == MFRC522::STATUS_OK) {
        status = mfrc522.MIFARE_Read(4, blk_buf, &len);
        if (status != MFRC522::STATUS_OK) {
            Serial.print(F("Reading failed: "));
            Serial.println(mfrc522.GetStatusCodeName(status));
        }
        att->id = *(uint16_t *)blk_buf;
        status = mfrc522.MIFARE_Read(5, blk_buf, &len);
        if (status != MFRC522::STATUS_OK) {
            Serial.print(F("Reading failed: "));
            Serial.println(mfrc522.GetStatusCodeName(status));
        }
        for (int i = 0; i < 16; i++) {
            att->sname[i] = blk_buf[i];
            if (!blk_buf[i]) break;
            if (i == 15) att->sname[i] = 0;
        }
        status = mfrc522.MIFARE_Read(6, blk_buf, &len);
        if (status != MFRC522::STATUS_OK) {
            Serial.print(F("Reading failed: "));
            Serial.println(mfrc522.GetStatusCodeName(status));
        }
        for (int i = 0; i < 16; i++) {
            att->fname[i] = blk_buf[i];
            if (!blk_buf[i]) break;
            if (i == 15) att->fname[i] = 0;
        }
       
    } else {
        Serial.print(F("Authentication failed: "));
        Serial.println(mfrc522.GetStatusCodeName(status));
    }
    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();
}

void print_attendee(attendee *att) {
    Serial.print(att->id);
    Serial.print(" ");
    Serial.println(String(att->sname) + " " + String(att->fname));
}

