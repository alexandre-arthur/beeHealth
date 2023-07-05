import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class BeeLineFinder {
    public static void main(String[] args) {
        File folder = new File("BeeDataset/FromWeb");
        File[] listOfFiles = folder.listFiles();

        int sizeOfExtension = 4;
        ArrayList<String> fileNames = new ArrayList<>();
        for(File listOfFile : listOfFiles) {
            if (listOfFile.getName().contains("lab")) {
                int fileNameLength = listOfFile.getName().length();
                fileNames.add(listOfFile.getName().substring(0, fileNameLength - sizeOfExtension));
            }
        }
        for (String fileName : fileNames) {
            System.out.println("Starting " + fileName);
            parseAFile(fileName);
            System.out.println(fileName + " is done.");
        }
    }

    public static void parseAFile(String fileName) {
        String genericFilePath = "BeeDataset/FromWeb/" + fileName;
        String dataFilePath = genericFilePath + ".lab"; // Update with the actual file path
        String audioFilePath = genericFilePath + ".wav";

        int lineWithBees = 0;
        ArrayList<Double> beginTimeStamps = new ArrayList<>();
        ArrayList<Double> endTimeStamps = new ArrayList<>();
        // Read the lab file
        try (BufferedReader reader = new BufferedReader(new FileReader(dataFilePath))) {
            String line;

            for(int lineNumber = 1; (line = reader.readLine()) != null; lineNumber++) {
                if (line.contains("bee") && !line.contains("nobee")) {
                    String[] parts = line.split("\t");
                    String number1Str = parts[0].replace(",", ".");
                    String number2Str = parts[1].replace(",", ".");
                    double number1 = Double.parseDouble(number1Str);
                    double number2 = Double.parseDouble(number2Str);
                    beginTimeStamps.add(number1);
                    endTimeStamps.add(number2);
                    lineWithBees++;
                    System.out.println("Line " + lineNumber + ": Number1=" + number1 + ", Number2=" + number2);
                }
            }
        } catch (IOException e) {
            System.err.println("Error reading the file: " + e.getMessage());
        }

        // Write the audio file sliced
        String pathName = "BeeDataset/OnlyBees/";
        for(int i = 0; i < lineWithBees; i++) {
            AudioFileProcessor.copyAudio(audioFilePath,
                    pathName + fileName + "_" + i + ".wav",
                    beginTimeStamps.get(i).intValue(),
                    endTimeStamps.get(i).intValue() - beginTimeStamps.get(i).intValue());
        }
    }
}