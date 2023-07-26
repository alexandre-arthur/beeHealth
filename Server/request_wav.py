import requests

# Set destination URL and file path here
url = 'http://127.0.0.1:5000/upload'
file_path = '/home/alexandre/Bureau/Documents/beeHealth/Server/static/sound/beeSound.wav'

try:
    # Open the WAV file in binary mode and read its content
    with open(file_path, 'rb') as wav_file:
        files = {'wav_file': wav_file}
        
        # Send the HTTP POST request with the WAV file as part of the payload
        response = requests.post(url, files=files)

    # Check the response status code to see if the upload was successful
    if response.status_code == 200:
        print("File successfully uploaded.")
    else:
        print("File upload failed. Status code:", response.status_code)

except FileNotFoundError:
    print("File not found. Please check the file path.")
except requests.RequestException as e:
    print("An error occurred during the file upload:", e)
