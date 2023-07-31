from flask import Flask, render_template, request
import datetime
import os
import shutil
import librosa
import globalClassRepresentation as gcr

app = Flask(__name__)

@app.route('/')
@app.route('/beeHealth_main.html')
def beeHealth_main():
    return render_template('beeHealth_main.html')

# Generate the route for the beeHealth_data.html file
@app.route('/beeHealth_data.html')   
def beeHealth_data():
    # Get the list of folders in the static/uploads directory
    folders = os.listdir('static/uploads')
    
    # Initialize an empty list to store sound table information
    sound_tables = []
    
    for folder_name in folders:
        # Extract information from the folder name (assuming folder_name has the format "13-12-25-07-2023")
        time = folder_name
        location = "Oulu"  # Replace with the actual location information if available
        link = folder_name + ".html"
        
        # Append the information to the sound_tables list
        sound_tables.append({
            'time': time,
            'location': location,
            'link': link
        })
    
    #give the list a reverse order to have the most recent data first
    #sound_tables.reverse()

    # Pass the sound_tables list to the template for rendering
    return render_template('beeHealth_data.html', sound_tables=sound_tables)

def copy_file_in_template_directory(source_file_name, new_file_name):
    try:
        # Get the absolute path of the source file
        source_file_path = os.path.abspath(source_file_name)

        # Get the path of the "templates" folder in the current directory
        templates_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

        # Get the absolute path of the destination file in the "templates" folder
        destination_file_path = os.path.join(templates_folder_path, new_file_name)

        # Copy the source file to the destination path
        shutil.copy(source_file_path, destination_file_path)

        print(f"The file '{source_file_name}' has been copied as '{new_file_name}' in the 'templates' folder.")
    except FileNotFoundError:
        print("The source file does not exist.")
    except PermissionError:
        print("Permission denied to copy the file.")
    except Exception as e:
        print(f"An error occurred: {e}")

def generateFFT(folder_name): 
    fft =  cr.FFTclass() 
    data, sampleRate = librosa.load('static/uploads/' + folder_name + '/' + folder_name + '_beeSound.wav')
    fft.createImage('static/uploads/' + folder_name+'/'+'fft.png', data, sampleRate)



# Generate the route for each analysis HTML file
@app.route('/<folder_name>.html')
def beeHealth_analysis(folder_name):
    source_file_name = "templateAnalysis.html"
    new_file_name = folder_name + ".html"

    copy_file_in_template_directory(source_file_name, new_file_name)

    generatePictures = gcr.GlobalClassRepresentation()
    generatePictures.getAllPictures('static/uploads/' + folder_name + '/', folder_name + '_beeSound.wav')


    return render_template(folder_name + '.html', path='uploads/' + folder_name)

@app.route('/beeHealth_about.html')
def beeHealth_about():
    return render_template('beeHealth_about.html')

@app.route('/beeHealth_contact.html')
def beeHealth_contact():
    return render_template('beeHealth_contact.html')

# Get the file from the client
@app.route('/upload', methods=['POST'])
def upload():
    if 'wav_file' not in request.files:
        return 'No file part in the request', 400
    
    wav_file = request.files['wav_file']
    if wav_file.filename == '':
        return 'No WAV file selected', 400
    
    # Get the current date and time
    current_datetime = datetime.datetime.now()
    
    # Format the date and time as "second_minute_hour_day_month_year"
    formatted_datetime = current_datetime.strftime("%S_%M_%H_%d_%m_%Y")
    
    # Create a new folder using the formatted date and time
    folder_name = formatted_datetime
    folder_path = os.path.join('static/uploads/', folder_name)
    os.makedirs(folder_path)
    
    # Modify the filename by adding the current date and time
    filename = formatted_datetime + "_" + wav_file.filename
    
    # Save the WAV file inside the new folder
    wav_file.save(os.path.join(folder_path, filename))

    return 'File successfully uploaded', 200

if __name__ == '__main__':
    app.run(debug=True)
