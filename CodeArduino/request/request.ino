#include <WiFi.h>
#include <HTTPClient.h>
#include <SD.h>

const char* ssid = "Votre_SSID";
const char* password = "Votre_Mot_de_passe";
const char* serverUrl = "http://votre_serveur.com/upload"; // URL du serveur qui recevra le fichier WAV

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Initialiser la carte SD
  if (!SD.begin()) {
    Serial.println("Erreur lors de l'initialisation de la carte SD");
    return;
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Remplacez "chemin_du_fichier" par le chemin de votre fichier WAV sur la carte SD
    File file = SD.open("/chemin_du_fichier", FILE_READ);

    if (!file) {
      Serial.println("Erreur lors de l'ouverture du fichier !");
      return;
    }

    // Démarrer une requête HTTP POST
    http.begin(serverUrl);
    http.addHeader("Content-Type", "audio/wav");

    // Envoyer le contenu du fichier WAV dans le corps de la requête
    int httpResponseCode = http.sendRequest("POST", file, file.size());

    // Fermer le fichier
    file.close();

    // Vérifier la réponse du serveur
    if (httpResponseCode == HTTP_CODE_OK) {
      Serial.println("Fichier WAV envoyé avec succès !");
    } else {
      Serial.print("Erreur lors de l'envoi du fichier. Code d'erreur : ");
      Serial.println(httpResponseCode);
    }

    // Libérer les ressources
    http.end();
  } else {
    Serial.println("Connexion WiFi perdue. Réessayez...");
  }

  // Attendre avant d'envoyer le fichier suivant (si nécessaire)
  delay(5000);
}
