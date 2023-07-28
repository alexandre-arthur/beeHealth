import os
import wave
import re
import math
import numpy as np
import librosa as rosa
import time

def main():
    t = time.time()
    tt = time.time()
    folder_path = "Representation/BeeDataset/FromWeb"
    size_of_extension = 4

    # Only take files with lab files
    file_names = []
    for file_name in os.listdir(folder_path):
        if "wav" in file_name:
            file_names.append(file_name[:-size_of_extension])

    # Parse every file
    counter = 0
    for file_name in file_names[1:-1]:
        counter += 1
        #if True :
        #file_name = file_names[10]
        print(f"Starting {file_name}")
        t = time.time()
        parse_a_file(file_name)
        print(f"{file_name} is done in {time.time() - t}s ({counter}/{len(file_names[1:-1])})")
    print(f"Everything is done in {time.time() - tt}s")

def readPartOfAudio(source_file_name, destination_file_name, start_second, seconds_to_copy):
    with wave.open(source_file_name, 'rb') as wave_file:
        frames_per_second = wave_file.getframerate()

        frames_to_skip = int(start_second * frames_per_second)
        frames_to_copy = int(seconds_to_copy * frames_per_second)

        try:
            wave_file.setpos(frames_to_skip)
        except:
            return None

        file = 0

        with wave.open(destination_file_name, 'wb') as output_file:
            output_file.setnchannels(wave_file.getnchannels())
            output_file.setsampwidth(wave_file.getsampwidth())
            output_file.setframerate(wave_file.getframerate())

            frames_wanted = wave_file.readframes(frames_to_copy)
            
            file = output_file.writeframes(frames_wanted)

        return 1

def parse_a_file(file_name):
    current_path = "DeepLearning/NeuralHivework/"
    timeDuration = 10
    maxFreq = 5000

    # Reader path
    generic_file_path = f"Representation/BeeDataset/FromWeb/{file_name}"
    data_file_path = f"{generic_file_path}.lab"
    audio_file_path = f"{generic_file_path}.wav"

    # Read the lab file
    with open(data_file_path, 'r') as reader:
        for line_number, line in enumerate(reader, start=1):
            bee = None
            if "bee" in line and "nobee" not in line:
                bee = 1
            elif "nobee" in line:
                bee = 0
            else:
                continue

            parts = re.split(r'\t+', line)
            number1_str = parts[0].replace(",", ".")
            number2_str = parts[1].replace(",", ".")
            begin = int(math.ceil(float(number1_str)))
            end = int(float(number2_str))
            
            for time in range(begin, end - 10, 10):
                #print(f"Line {line_number}: begin={time}, end={time + timeDuration}")

                r = readPartOfAudio(audio_file_path, f"{current_path}Processing.wav", time, timeDuration)
                if(r == None):
                    continue
                file , sample_rate = rosa.load(f"{current_path}Processing.wav")
                fft_data = np.fft.fft(file)
                # Calculate the magnitudes of the FFT coefficients
                magnitudes = np.abs(fft_data)
                magnitudes = magnitudes[:(int) (magnitudes.size/(20000 / maxFreq))] # Only upto a certain frequency
                toWrite = ",".join(str(value) for value in magnitudes) + "," + str(bee) + "\n"

                with open(f"{current_path}FastHoneyTransform.csv", "a") as file:
                    if magnitudes.size != 55125:
                        print(f"{magnitudes.size} value in line : {line_number} in file : {file_name}")
                        continue
                    file.write(toWrite)


if __name__ == "__main__":
    main()
