/*
 * DJ WHEEL CONTINUOUS MOTION OUTPUT (PRODUCTION)
 *
 * Output format (every REPORT_MS):
 *   COUNT:<signed_count>|DT:<ms>|RPM:<signed_rpm>
 *
 * --- SETUP REQUIRED ---
 * - Set your encoder pins (PIN_A, PIN_B)
 * - Set your encoder resolution (COUNTS_PER_REV)
 *
 * Arduino Uno compatible.
 */

#include <Arduino.h>

volatile long encoderCount = 0;

// ---- PIN CONFIG ----
// INSERT YOUR ENCODER PINS (must support interrupts on your board)
const int PIN_A = 2;
const int PIN_B = 3;

// ---- ENCODER CALIBRATION ----
// INSERT YOUR ENCODER COUNTS PER REVOLUTION
// (measure this for your specific encoder / gearing setup)
const float COUNTS_PER_REV = 2000.0;

// ---- TIMING ----
const unsigned long REPORT_MS = 50;        // 20 Hz output
const unsigned long STOP_TIMEOUT_MS = 200; // no pulses => rpm=0

// ---- STATE ----
unsigned long lastReportMs = 0;
unsigned long lastPulseMs  = 0;

void countA() {
  bool a = digitalRead(PIN_A);
  bool b = digitalRead(PIN_B);
  if (a == b) encoderCount++;
  else        encoderCount--;
}

void setup() {
  Serial.begin(115200);

  pinMode(PIN_A, INPUT_PULLUP);
  pinMode(PIN_B, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(PIN_A), countA, CHANGE);

  lastReportMs = millis();
  lastPulseMs  = millis();

  Serial.println("DJ WHEEL MOTION STREAM READY");
}

void loop() {
  unsigned long now = millis();

  if (now - lastReportMs >= REPORT_MS) {
    long count;

    noInterrupts();
    count = encoderCount;
    encoderCount = 0;
    interrupts();

    if (count != 0) lastPulseMs = now;

    unsigned long dt_ms = now - lastReportMs;
    float rpm = 0.0f;

    if (now - lastPulseMs > STOP_TIMEOUT_MS) {
      rpm = 0.0f;
      count = 0;
    } else {
      float revs = (float)count / COUNTS_PER_REV;
      float minutes = (float)dt_ms / 60000.0f;
      if (minutes > 0.0f) rpm = revs / minutes;
    }

    Serial.print("COUNT:");
    Serial.print(count);
    Serial.print("|DT:");
    Serial.print(dt_ms);
    Serial.print("|RPM:");
    Serial.println(rpm, 3);

    lastReportMs = now;
  }
}
