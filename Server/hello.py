from flask import Flask, render_template, request

app = Flask(__name__)

#generate the route for each html file from the template folder
@app.route('/')
@app.route('/beeHealth_main.html')
def beeHealth_main():
    return render_template('beeHealth_main.html')

@app.route('/beeHealth_data.html')   
def beeHealth_data():
    return render_template('beeHealth_data.html')

@app.route('/beeHealth_about.html')
def beeHealth_about():
    return render_template('beeHealth_about.html')

@app.route('/beeHealth_contact.html')
def beeHealth_contact():
    return render_template('beeHealth_contact.html')

#generate autamatically the route for each analysis html file !
@app.route('/13-12-25-07-2023.html')
def beeHealth_13_12_25_07_2023():
    return render_template('13-12-25-07-2023.html')

#get the file from the clientcl
@app.route('/upload', methods=['POST'])
def upload():
    if 'wav_file' not in request.files:
        return 'No file part in the request', 400
    
    wav_file = request.files['wav_file']
    if wav_file.filename == '':
        return 'No WAV file selected', 400
    
    wav_file.save('uploads/' + wav_file.filename)
    return 'File successfully uploaded', 200

if __name__ == '__main__':
    app.run(debug=True)
