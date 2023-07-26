from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/beeHealth_main.html')
def beeHealth_main():
    return render_template('beeHealth_main.html')

@app.route('/beeHealth_data.html')   
def beeHealth_data():
    return render_template('beeHealth_data.html')

#generate autamatically the route for each analysis html file !
@app.route('/13-12-25-07-2023.html')
def beeHealth_13_12_25_07_2023():
    return render_template('13-12-25-07-2023.html')



if __name__ == '__main__':
    app.run(debug=True)
