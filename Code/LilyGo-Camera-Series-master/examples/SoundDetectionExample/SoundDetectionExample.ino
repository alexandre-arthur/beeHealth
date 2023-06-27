#include <Wire.h>
#include <driver/i2s.h>

#define SAMPLE_RATE 44100   // Fréquence d'échantillonnage du microphone
#define I2S_WS 42           // Broche IO42 pour MIC_WS
#define I2S_SCK 41          // Broche IO41 pour MIC_SCK
#define I2S_DATA 2          // Broche IO02 pour MIC_DATA

void setup() {
  Serial.begin(9600);
  
  // Configuration de l'I2S
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_RIGHT,
    .communication_format = I2S_COMM_FORMAT_I2S_MSB,
    .intr_alloc_flags = 0,
    .dma_buf_count = 8,
    .dma_buf_len = 64,
    .use_apll = false,
    .tx_desc_auto_clear = false,
    .fixed_mclk = 0
  };
  
  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_DATA
  };
  
  i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pin_config);
}

void loop() {
  int32_t samples[64];  // Tableau pour stocker les échantillons audio
  
  // Lecture des échantillons audio du microphone I2S
  i2s_read(I2S_NUM_0, (void *)samples, sizeof(samples), NULL, portMAX_DELAY);
  
  // Affichage des échantillons sur le moniteur série
  for (int i = 0; i < sizeof(samples) / sizeof(samples[0]); i++) {
    Serial.println(samples[i]);
  }

  delay(100);  // Attente de 100 millisecondes entre chaque lecture
}
