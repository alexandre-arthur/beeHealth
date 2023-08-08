import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class BeeLineFinder {
    public static void main(String[] args) {
        //Path to the folder containing the files
        String path = "Representation/BeeDataset/RawFilesFromWeb";
        File folder = new File(path);
        File[] listOfFiles = folder.listFiles();

        int sizeOfExtension = 4;
        ArrayList<String> fileNames = new ArrayList<>();
        // Get the file names without the extension
        for(File listOfFile : listOfFiles) {
            if (listOfFile.getName().contains("wav")) {
                int fileNameLength = listOfFile.getName().length();
                fileNames.add(listOfFile.getName().substring(0, fileNameLength - sizeOfExtension));
            }
        }
        for (String fileName : fileNames) {
            System.out.println("Starting " + fileName);
            parseAFile(fileName, path);
            System.out.println(fileName + " is done.");
        }
    }

    public static void parseAFile(String fileName, String readerPath) {
        // Reader path
        String genericFilePath = readerPath + "/" + fileName;
        String dataFilePath = genericFilePath + ".lab"; // Update with the actual file path
        String audioFilePath = genericFilePath + ".wav";

        // init Variables
        int lineWithBees = 0;
        ArrayList<Integer> beginTimeStamps = new ArrayList<>();
        ArrayList<Integer> endTimeStamps = new ArrayList<>();
        ArrayList<String> beeLines = new ArrayList<>();
        // Read the lab file
        try (BufferedReader reader = new BufferedReader(new FileReader(dataFilePath))) {
            String line;

            // read the lines one by one and get the time stamps
            for(int lineNumber = 1; (line = reader.readLine()) != null; lineNumber++) {
                if (line.contains("bee") && !line.contains("nobee")) {
                    beeLines.add("B");
                }
                else if(line.contains("nobee")) {
                    beeLines.add("N");
                }
                else {
                    continue;
                }
                System.out.println(dataFilePath);
                String[] parts = line.split("\t");
                String number1Str = parts[0].replace(",", ".");
                String number2Str = parts[1].replace(",", ".");
                double number1 = Double.parseDouble(number1Str);
                double number2 = Double.parseDouble(number2Str);
                int number1Int = (int) Math.ceil(number1);
                int number2Int = (int) Math.ceil(number2);
                beginTimeStamps.add(number1Int);
                endTimeStamps.add(number2Int);
                lineWithBees++;
                System.out.println("Line " + lineNumber + ": Number1=" + number1Int + ", Number2=" + number2Int);
            }
        } catch (IOException e) {
            System.err.println("Error reading the file: " + e.getMessage());
        }

        // Write the audio file sliced
        String pathName = "Representation/BeeDataset/TheBeetles/";
        for(int i = 0; i < lineWithBees; i++) {
            int begin = beginTimeStamps.get(i);
            int end = endTimeStamps.get(i);
            String name = beeLines.get(i);
            if(end != begin) {
            AudioFileProcessor.copyAudio(audioFilePath,
                    pathName + fileName + "_" + i + "_" + name + ".wav",
                    begin,
                    end - begin);
            }
        }
    }
}