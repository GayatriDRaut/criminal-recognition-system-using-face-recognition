
# Microsoft Engage Program 2022 (Face-Recognition Challenge)
**Problem Statement:**
To develop a browser based application to demonstrate the use of face- recognition.


## Criminal Identification System   
A web applicatiom developed to identify criminals using their photo and webcam, built using python's face-Recognition library.
   
## Video Demo
You can find the video demo of the app: https://youtu.be/9FvcQzpen5Y


## Features of the application
* Secure Login System (only admin users are allowed)
* Add Criminals to database
* Change their status (Wanted/Found)
* Identify Criminal from photos
* Identify Criminal in live cameras (webcam)
* Update Criminal location in the record with date and time of Detection



## How to run the application
### Installation requirements
First of all, clone the git hub repository on your machine.  
Make sure you have python downloaded, incase you haven't already visit this link: https://www.python.org/downloads/  

To install the required packages use the following command

```bash
 pip install -r requirements.txt
```
Libraries and Framework used:  
Python == 3.6.15   
Django == 3.2.3   
Django Rest Framework == 3.13.1 
Numpy == 1.18.4 
OpenCV == 4.5.5.64  
Pillow == 5.4.1
Dlib == 19.22.0  
face-recognition == 1.3.0  
opencv_python_headless == 4.5.5.64 
JQuery   
mySQL database 

In settings.py file change the variable DATABASES:

```bash
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/path/to/my.cnf',
        },
    }
}


# my.cnf
[client]
database = NAME
user = USER
password = PASSWORD
default-character-set = utf8
```



To start the app
```bash
 python manage.py runserver
```
And open http://127.0.0.1:8000/ at your system



## Steps to navigate the website
**1)Login Page**
To login enter the following credentials  
**Police EmailID : gayatri@gmail.com**    
**Password: gayatri**  
Hit the Login buttton to enter the website   
         
       
**2)Add Criminals**
Under the criminals tab you will see add criminals tab, it will open a form wherein you have to fill criminal data, their photo to register them to the website.  
     
       
**3)View Criminals**
Right below the add criminals tab, view criminals tab allows the user to view the data of the criminals present in the database.  
   
    
**4) Identify Criminals**
Two options are avialable to identify criminals that is to use a photo and the system will detect if their face is present there or not.
And the second option is to detect the criminal using webcam.   
      
      
 **5)Track Criminals**   
 After detecting the criminals in live cameras the webiste updates the database with the last spotted location and time of the criminal.








    
## Screenshots
### Log In Page of the website
![App Screenshot](screenshots/login.jpg?raw=true "Log In Page")  
### Dashboard/Identify Criminals
![App Screenshot](screenshots/dashboard.jpg?raw=true "Log In Page")  
### For viewing criminals in the Database
![App Screenshot](screenshots/view_criminals.jpg?raw=true "Log In Page")  
### Identify criminal in the database with webcam
![App Screenshot](screenshots/webcam.png?raw=true "Log In Page")     
### Last Spotted Criminal with date and time
![App Screenshot](screenshots/track_criminals.jpg?raw=true "Log In Page")    

