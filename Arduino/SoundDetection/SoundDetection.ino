#include <driver/i2s.h>

// I2S microphone pin configuration
const int I2S_WS = 42;  // Word Select (WS) pin
const int I2S_SD = 2;   // Serial Data (SD) pin
const int I2S_SCK = 41; // Serial Clock (SCK) pin

// I2S configuration
const i2s_port_t I2S_PORT = I2S_NUM_0;                               // I2S port to use
const int SAMPLE_RATE = 44100;                                       // Sampling rate in Hz
const int BITS_PER_SAMPLE = 16;                                      // Bits per sample
const i2s_channel_fmt_t CHANNEL_FORMAT = I2S_CHANNEL_FMT_ONLY_LEFT;  // Channel format (mono)
const i2s_comm_format_t COMM_FORMAT = I2S_COMM_FORMAT_STAND_I2S;     // Standard I2S communication format
const int DMA_BUFFER_COUNT = 8;                                      // Number of DMA buffers to use
const int DMA_BUFFER_LEN = 64;                                       // Length of each DMA buffer
const size_t SAMPLE_SIZE = sizeof(int16_t);                          // Size of one sample in bytes

int16_t sBuffer[DMA_BUFFER_LEN];  // Buffer for audio samples


void setupI2S() {
  // I2S configuration
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),     // Master mode for receiving
    .sample_rate = SAMPLE_RATE,                              // Sampling rate
    .bits_per_sample = (i2s_bits_per_sample_t)BITS_PER_SAMPLE, // Bits per sample
    .channel_format = CHANNEL_FORMAT,                        // Audio channel format
    .communication_format = COMM_FORMAT,                      // Communication format
    .intr_alloc_flags = 0,                                    // Interrupt allocation flags
    .dma_buf_count = DMA_BUFFER_COUNT,                        // Number of DMA buffers
    .dma_buf_len = DMA_BUFFER_LEN,                            // Length of each DMA buffer
    .use_apll = false                                         // Use APLL (Audio PLL)
  };

  // Install the I2S driver with the specified configuration
  i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);

  // I2S pin configuration
  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,                                   // Serial Clock (SCK) pin
    .ws_io_num = I2S_WS,                                     // Word Select (WS) pin
    .data_out_num = -1,                                      // No data output
    .data_in_num = I2S_SD                                    // Serial Data (SD) pin
  };

  // Assign I2S pins to the specified I2S port
  i2s_set_pin(I2S_PORT, &pin_config);
}

void setupSerial() {
  // Initialize serial communication
  Serial.begin(115200);   // Communication speed of 115200 bauds
  Serial.println("Start");  // Print "Start" message to the serial monitor
  delay(1000);            // Wait for a second to allow stable connection
}

void setup() {
  setupSerial();     // Call the function to set up serial communication
  setupI2S();        // Call the function to set up I2S
}

void loop() {
  readMic();    // Call the function to read audio data from the I2S microphone
  //sendAudioData(); 
}

void readMic() {
  size_t bytesIn = 0;  // Variable to store the number of bytes read
  esp_err_t result = i2s_read(I2S_PORT, &sBuffer, DMA_BUFFER_LEN * SAMPLE_SIZE, &bytesIn, portMAX_DELAY);
  // Read audio data from the I2S microphone and store it in the sBuffer data buffer
  // The read size is defined by DMA_BUFFER_LEN * SAMPLE_SIZE, which corresponds to the buffer size in bytes
  // The number of bytes read is stored in the bytesIn variable

  if (result == ESP_OK) {
    // If the read operation is successful
    int16_t samplesRead = bytesIn / SAMPLE_SIZE;
    // Calculate the number of samples read by dividing the total number of bytes read by the size of one sample in bytes

    if (samplesRead > 0) {
      // If samples have been read
      float mean = 0;  // Variable to calculate the mean of the samples

      for (int16_t i = 0; i < samplesRead; ++i) {
        mean += sBuffer[i];  // Accumulate the samples to calculate the total sum
      }

      mean /= samplesRead;  // Calculate the mean by dividing the total sum by the number of samples

      Serial.println(mean);  // Print the mean value to the serial monitor
    }
  } else {
    // If an error occurred during the I2S read operation
    handleI2SError(result);  // Call the function to handle the I2S error
  }
}

void sendAudioData() {
  size_t bytesIn = 0;  // Variable to store the number of bytes read
  esp_err_t result = i2s_read(I2S_PORT, &sBuffer, DMA_BUFFER_LEN * SAMPLE_SIZE, &bytesIn, portMAX_DELAY);
  // Read audio data from the I2S microphone and store it in the sBuffer data buffer
  // The read size is defined by DMA_BUFFER_LEN * SAMPLE_SIZE, which corresponds to the buffer size in bytes
  // The number of bytes read is stored in the bytesIn variable

  if (result == ESP_OK) {
    // If the read operation is successful
    int16_t samplesRead = bytesIn / SAMPLE_SIZE;
    // Calculate the number of samples read by dividing the total number of bytes read by the size of one sample in bytes

    if (samplesRead > 0) {
      // If samples have been read
      float mean = 0;  // Variable to calculate the mean of the samples

      for (int16_t i = 0; i < samplesRead; ++i) {
        mean += sBuffer[i];  // Accumulate the samples to calculate the total sum
      }

      mean /= samplesRead;  // Calculate the mean by dividing the total sum by the number of samples
      
      // Convert the mean value to bytes
      int16_t meanValue = (int16_t)mean;
      uint8_t* meanBytes = (uint8_t*)&meanValue;

      // Send the mean value bytes via Serial
      for (int i = 0; i < sizeof(meanValue); ++i) {
        Serial.write(meanBytes[i]);
      }
    }
  } else {
    // If an error occurred during the I2S read operation
    handleI2SError(result);  // Call the function to handle the I2S error
  }
}


void handleI2SError(esp_err_t error) {
  Serial.print("I2S error: ");  // Print the generic error message

  switch (error) {
    case ESP_ERR_INVALID_ARG:
      Serial.println("Invalid argument");  // Error: invalid argument
      break;
    case ESP_ERR_NOT_FOUND:
      Serial.println("Not found");  // Error: not found
      break;
    case ESP_ERR_INVALID_STATE:
      Serial.println("Invalid state");  // Error: invalid state
      break;
    case ESP_ERR_TIMEOUT:
      Serial.println("Timeout");  // Error: timeout
      break;
    case ESP_ERR_INVALID_SIZE:
      Serial.println("Invalid size");  // Error: invalid size
      break;
    case ESP_ERR_NOT_SUPPORTED:
      Serial.println("Not supported");  // Error: not supported
      break;
    case ESP_ERR_INVALID_RESPONSE:
      Serial.println("Invalid response");  // Error: invalid response
      break;
    case ESP_ERR_INVALID_CRC:
      Serial.println("Invalid CRC");  // Error: invalid CRC
      break;
    case ESP_ERR_INVALID_VERSION:
      Serial.println("Invalid version");  // Error: invalid version
      break;
    case ESP_ERR_INVALID_MAC:
      Serial.println("Invalid MAC address");  // Error: invalid MAC address
      break;
    default:
      Serial.println("Unknown error");  // Unknown error
      break;
  }
}
