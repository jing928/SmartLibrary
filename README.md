# Smart Library Management System
RMIT Programming Internet of Things Assignment 2

by *Quan Cheng*, *Yanan Guo*, *Jing Li*, *Cheng Qian*

## Introduction

A Smart Library System Built for Raspberry Pi. The system can be used to facilitate everyday operations of a library. 
For the system to work, two Raspberry Pi's are required with one being the Master Pi and the other being the Reception Pi.

The Reception Pi handles user registration and user login, while the Master Pi handles main functions,
such as Search, Borrow, and Return a book.

To login to the system, the user can either choose to manually type in the credentials ro to use
facial recognition provided they have had their faces scanned beforehand.

Once logged in, the user can search for books to borrow. The user can either type in the search query
or use the voice recognition to search. When returning a borrowed book, the user can choose to manually 
enter the book ID or scan the QR code of the book.

For library admin, the system also provides a web app that allows the admin to add new books and to delete
books. Besides, the admin can also view the borrow & return statistics for a specific time period.


## Instalation

1. SSH into the Raspbian and run `mkdir Workspaces`
1. Run cd Workspaces and then git clone this repository.

### Dependencies

Run the following to install all required dependencies:

1. `sudo apt-get install sqlite3`
1. `pip3 install pymysql`
1. `pip3 install tabulate`
1. `pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
1. `pip3 install SpeechRecognition`
1. `sudo apt-get install portaudio19-dev python-all-dev python3-all-dev`
1. `pip3 install pyaudio`
1. `sudo apt-get install flac`
1. `pip3 install pyzbar`
1. `sudo apt-get install build-essential cmake pkg-config`
1. `sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev`
1. `sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev`
1. `sudo apt-get install libxvidcore-dev libx264-dev`
1. `sudo apt-get install libgtk2.0-dev libgtk-3-dev`
1. `sudo apt-get install libcanberra-gtk*`
1. `sudo apt-get install libatlas-base-dev gfortran`
1. `sudo apt-get install python2.7-dev python3-dev`
1. `pip3 install numpy`
1. `sudo apt-get install python3-picamera`
1. `pip3 install --upgrade picamera[array]`
1. `pip3 install dlib`
1. `pip3 install face_recognition`
1. `pip3 install imutils`
1. `pip3 install Flask`
1. `pip3 install flask_sqlalchemy`
1. `pip3 install flask_marshmallow`




## Configuration

### Create Cloud SQL Database

To use the system, one must first create a MySQL database, preferably with one of cloud service provides,
such as Google Cloud Platform. Then create a `db_config.json` file in the root directory of this
project with following information.

```json
{
    "HOST": "<Host Name>",
    "USER": "<User Name",
    "PASSWORD": "<Password>",
    "DATABASE": "<DB Name"
}
``` 

### Create Master Pi IP Configuration

For the Reception Pi to communicate with the Master Pi, one must provide an `ip_config.json` file
in the root directory of this project with the following information.

```json
{
  "ip": "<IP Address of the Master Pi>"
}

```

### Setup Audio/Video Device Configuration

The Smart Library System comes with two USB cameras (**Microsoft® LifeCam HD-3000**) to enable for
facial and voice search functionality.

For the Pi to know the default device, one must add the `.asoundrc` file to the home direction of the Pi.

```
pcm.!default {
  type asym
  capture.pcm "mic"
  playback.pcm "speaker"
}
pcm.mic {
  type plug
  slave {
    pcm "hw:1,0"
  }
}
pcm.speaker {
  type plug
  slave {
    pcm "hw:0,0"
  }
}
```
 
### Setup Google Calendar API

The system automatically creates event on due date when a customer borrows a book on the Google Calendar, therefore,
one must obtain a `credentials.json` file from Google Calendar API and add it to the root directory
of this project.



## Usage

### Reception Pi

To start the Reception Pi console program, simply run the following on one of the Pi's:
```bash
python3 reception_pi_app.py
```

Then the main menu will display in the terminal.

### Master Pi

On the other Pi, run the following:
```bash
python3 master_pi_app.py
```

Then this will start the Master Pi console and the Master Pi will continue listening to signals
sent by the Reception Pi. Whenever a user logs in on the Reception Pi, the main menu of the 
Master Pi will be activated.

### Admin Web App

On the Master Pi, first change the `HOST_URL` in the `webapp/config.py` to be the IP address
of the Master Pi. Then run the following:
```bash
python3 webapp/flask_main.py
``` 

## Documentation

Please view the website for Sphinx Documentation: [Go](http://smartlibrary.epizy.com/)