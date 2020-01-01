# Pop-Share Fun_blog
## Introduction
This is a very basic blog built with python's flask framework. Some of the features include registering to create a profile, login-in, upload profile picture and upload what's on your mind in a text box, content can also be deleted. Password reset is also an included feature through the user's mail. There are available restfulAPIs for each users posts. The most exciting feature of the app is the user can post a picture, and the mood of the person in the picture is detected using a pre-trained Facial Entity Recognizer model.
## Dependency
- Python3, Ubuntu 18.04
- Flask and other 3rd party libraries including; Flask-Sqlalchemy, Flask-Bcrypt, Flask-Lgin, Flask-Mail
- OpenCV, Tensorflow, Keras, Pillow
- To install the required packages, run pip install -r requirements.txt
## Pretrained Model
Download the Keras pretrained model here https://drive.google.com/file/d/0B6yZu81NrMhSV2ozYWZrenJXd1E/view?usp=sharing and put in the Pop-Share directory
## Usage
- First, clone the repository with git clone https://github.com/Pydare/Pop-Share.git and enter the cloned folder: cd Pop-Share.
- Change the environment variables using bash
- Create a local Sqlite RDBMS. More guide here: https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
- Create your server using python run.py and open the link in your browser: localhost:5000
