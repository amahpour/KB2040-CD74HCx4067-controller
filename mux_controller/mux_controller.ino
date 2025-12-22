// CD74HC4067 Multiplexer Controller for KB2040
// Controls 16-channel mux via GPIO pins 2-5 (S0-S3)
// Note: GPIO pin 1 doesn't work, so pins shifted by 1
// Serial commands: CH n (0-15), STATUS/?, HELP

// Pin definitions for CD74HC4067 select lines
// Hardware mapping: Pin 2 → S0, Pin 3 → S1, Pin 4 → S2, Pin 5 → S3
#define S0_PIN 2  // LSB - GPIO pin 2 → S0
#define S1_PIN 3  // GPIO pin 3 → S1
#define S2_PIN 4  // GPIO pin 4 → S2
#define S3_PIN 5  // MSB - GPIO pin 5 → S3

uint8_t currentChannel = 0;

void setup() {
  // Initialize GPIO pins as outputs
  // Note: Ensure pins are configured before Serial.begin() to avoid conflicts
  pinMode(S0_PIN, OUTPUT);
  pinMode(S1_PIN, OUTPUT);
  pinMode(S2_PIN, OUTPUT);
  pinMode(S3_PIN, OUTPUT);
  
  // Set initial state (all LOW for channel 0)
  digitalWrite(S0_PIN, LOW);
  digitalWrite(S1_PIN, LOW);
  digitalWrite(S2_PIN, LOW);
  digitalWrite(S3_PIN, LOW);
  
  // Initialize serial communication (USB CDC, doesn't use GPIO 0/1)
  Serial.begin(115200);
  
  // Wait for serial connection (optional, remove if you want immediate startup)
  while (!Serial) {
    delay(10);
  }
  
  // Set initial channel to 0
  setChannel(0);
  
  Serial.println("CD74HC4067 Controller Ready");
  Serial.println("Commands: CH n (0-15), STATUS/?, HELP");
}

void loop() {
  // Check for incoming serial data
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();  // Remove whitespace
    command.toUpperCase();  // Convert to uppercase for case-insensitive parsing
    
    if (command.length() > 0) {
      processCommand(command);
    }
  }
}

void processCommand(String cmd) {
  // Parse CH command: "CH 5" or "CH5"
  if (cmd.startsWith("CH")) {
    // Extract channel number
    int spaceIndex = cmd.indexOf(' ');
    int channel;
    
    if (spaceIndex > 0) {
      // Format: "CH 5"
      channel = cmd.substring(spaceIndex + 1).toInt();
    } else if (cmd.length() > 2) {
      // Format: "CH5"
      channel = cmd.substring(2).toInt();
    } else {
      Serial.println("ERR:RANGE");
      return;
    }
    
    // Validate channel range
    if (channel >= 0 && channel <= 15) {
      setChannel(channel);
      Serial.print("OK:");
      Serial.println(channel);
    } else {
      Serial.println("ERR:RANGE");
    }
  }
  // STATUS or ? command
  else if (cmd == "STATUS" || cmd == "?") {
    Serial.print("CH:");
    Serial.println(currentChannel);
  }
  // HELP command
  else if (cmd == "HELP") {
    Serial.println("CD74HC4067 Controller Commands:");
    Serial.println("  CH n      - Select channel (0-15)");
    Serial.println("  STATUS    - Show current channel");
    Serial.println("  ?         - Show current channel");
    Serial.println("  HELP      - Show this help");
  }
  // Unknown command
  else {
    Serial.println("ERR:CMD");
  }
}

void setChannel(uint8_t channel) {
  // Set GPIO pins based on binary representation of channel
  digitalWrite(S0_PIN, channel & 0x01);        // Bit 0 (LSB)
  digitalWrite(S1_PIN, (channel >> 1) & 0x01); // Bit 1
  digitalWrite(S2_PIN, (channel >> 2) & 0x01); // Bit 2
  digitalWrite(S3_PIN, (channel >> 3) & 0x01); // Bit 3 (MSB)
  
  currentChannel = channel;
}

