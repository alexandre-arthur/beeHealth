# BeeHealth Project
## Project presentation
This is a summer porject who aims to be able to listen to bees and detect any problem with a bee (queen missing, not enough food...). This project has been held so far by three students at the university of Oulu with th supervision of Juha Häkkinen, a professor at the university. 

Another goal was to be able to locate the bee around a flower to maybe get more information about them.

We have divided the project in X parts : 
- The audio in which we can put all the audio datasets to work on (Not on the github, more information below),
- The arduino code
- The deep learning that aimed to take transformed audios and to help recognize any problem with the bees,
- The documentation with all the study we used to work on this project,
- The representation to transform the sounds in other way to study it more precisely
- The server which is here to show all the sounds we collected

Everything is detailed under.

## Sommaire
[Test](#audio)


## Audio
This directory is the only one that doesn't exist when cloning the project. That is because the audio files are two big to go on the github. But you can donwload them on your computer, locally. 

To do so, you need to go to "Representation/AudioDownload/JSONDownload/" and to launch APIReaderJSON.py which reads the ToBeeOrNotToBee.json file and download all the files into the "/Audio" folder. It takes approximately 4 minutes and you need an internet connexion.


# Arduino
They are two folders : 
- SoundDetection : contain an arduino code to read the I2S mic and display the value to a graph thanks to arduino IDE 
- request : send resquest to a webserver with an esp32 

## Deep Learning


## Documentation


## Representation
To use this file, you must have the librosa library installed.

In this folder, you have :
- The folder to download all the audio to the Audio directory,
- The GlobalRepresentation folder which hold everything you need from this part:
    - "Filters.py" : function to use to filter specific frequency from an audio (50 Hz frequency for example) and Low/High Pass Filter,
    - "ClassRepresentation.py" : all the way to transform the sound possible (Wave, MFFCs...). 
    - "GlobalClassRepresentation.py" : Class with all the class created in "ClassRepresentation.py"
    - "GlobalFiguresBees.py" : Show all the representation in one plot. You may not use this function but use it via the app,
    - "App.py" : A non official app to study the sounds. Can show the sound in various ways. Became deprecated with the addition of the site.
    - "Images" : Images for the app

## Server
This part of the project is powered by Flask. Flask is a microservice that enables the creation of a web server using Python. One of the advantages of this approach is the flexibility to utilize a wide range of technologies.

In this project, we employ HTML and CSS. We have multiple templates, and thanks to the Jinja template engine, we can customize some aspects. For instance, on the data page, we exhibit all the sounds from the project, each linked to its corresponding analysis page.

### Folder Structure
- Main
    - hello.py: This script initializes the web server and contains functions to generate HTML pages.
    - request_wav.py: Responsible for sending WAV files to the server.

- Templates
The templates folder houses all dynamic files.
    - beeHealth_data.html: This template showcases all the sounds and provides links to their respective analysis pages.
    - beeHealth_contact.html: A contact page for the project.
    - beeHealth_about.html: Offers an explanation of the project.
    - beeHealth_main.html: The main landing page of the website.
    - templateAnalysis.html: A template for the analysis pages.

- Static
The static folder contains various static files, including sounds, CSS stylesheets, and images. 
