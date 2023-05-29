// Defineer de pinnen voor de motor van het 10 eurobiljet
const int motor10Pinnen[4] = {2, 3, 4, 5};
// Defineer de pinnen voor de motor van het 20 eurobiljet
const int motor20Pinnen[4] = {6, 7, 8, 9};
// Defineer de pinnen voor de motor van het 50 eurobiljet
const int motor50Pinnen[4] = {10, 11, 12, 13};

void setup() {
  Serial.begin(9600);
  
  // Configureer de motorpinnen als uitgang
  for (int i = 0; i < 4; i++) {
    pinMode(motor10Pinnen[i], OUTPUT);
    pinMode(motor20Pinnen[i], OUTPUT);
    pinMode(motor50Pinnen[i], OUTPUT);
  }
}

void loop() {
  if (Serial.available()) {
    // read the incoming byte:
    String incomingString = Serial.readStringUntil('\n');
    int spaceIndex1 = incomingString.indexOf(' ');
    int spaceIndex2 = incomingString.lastIndexOf(' ');

    String tensString = incomingString.substring(0, spaceIndex1);
    String twentiesString = incomingString.substring(spaceIndex1+1, spaceIndex2);
    String fiftiesString = incomingString.substring(spaceIndex2+1);
    
    int tens = tensString.toInt();
    int twenties = twentiesString.toInt();
    int fifties = fiftiesString.toInt();
    
    for (int i = 0; i < tens; i++){
      draaiMotor(motor10Pinnen);
    }
    for (int i = 0; i < twenties; i++){
      draaiMotor(motor20Pinnen);
    }
    for (int i = 0; i < fifties; i++){
      draaiMotor(motor50Pinnen);
    }
 
    Serial.println("done");
  }
}

void draaiMotor(int motorPinnen[4]) {
  // Definieer de stappen voor een volledige rotatie van 360 graden
  int stappen[8][4] = {
    {HIGH, LOW, LOW, LOW},
    {HIGH, HIGH, LOW, LOW},
    {LOW, HIGH, LOW, LOW},
    {LOW, HIGH, HIGH, LOW},
    {LOW, LOW, HIGH, LOW},
    {LOW, LOW, HIGH, HIGH},
    {LOW, LOW, LOW, HIGH},
    {HIGH, LOW, LOW, HIGH}
  };

  // Draai de motor voor een volledige rotatie
  for (int i = 0; i < 512; i++) {
    for (int j = 0; j < 8; j++) {
      for (int k = 0; k < 4; k++) {
        digitalWrite(motorPinnen[k], stappen[j][k]);
      }
      delay(2);
    }
  }

  // Zet alle pinnen van de motor laag om de motor te stoppen
  for (int i = 0; i < 4; i++) {
    digitalWrite(motorPinnen[i], LOW);
  }
}
