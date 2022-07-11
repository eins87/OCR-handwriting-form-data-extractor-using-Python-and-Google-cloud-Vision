# OCR handwriting "form jobsheet" data extractor using Python and Google cloud Vision
#### Video Demo:  https://youtu.be/ocDpP9oc0Ko
#### Description:
this webapps is using python and google cloud vision to ocr handwriting "form jobsheet". this can be used to convert the physical "form jobsheet" or old "form jobsheet" to digital "form jobsheet", because the function is to ocr the handwriting text to standard computer character. and the accuracy from google cloud vision for ocr-ing handwriting text is pretty high.
the upload folder is for hold the uploaded file "form jobsheet", name for the file is "jobsheet". in the "form jobsheet" it have many informations that is important for the company because it relatively to the history of the device. app.py is the main application program, it include the route and methods for the webapps.
in the app.py two routes is defined, index and upload, index for handle the user interface of main page in webapps, and upload for handle the upload proses and ocr-ing process including align uploaded image.

Technologies used:

- Google Cloud Vision API
- Flask
- opencv
- bootstrap
- jquery
- other libraries or packages

## Project Structure

project  
├── app  
│   ├── templates  
│   │   └── "form jobsheet"_jobsheet_template.jpg  
│   ├── upload  
│   └── symbolic-wind.json  
├── static  
│   ├── db  
│   │   └── ocrdata.db  
│   ├── js  
│   │   └── dropzone_config.js  
│   └── style.css  
├── templates  
│   ├── index.html  
│   └── layout.html  
├── README.md  
├── align_image.py  
├── app.py  
└── requirements.txt  

## How the webapps works?

The user download "form jobsheet" template, print it and file each field with handwriting then scan using scanner device or multi function printer which have scanner function as an image then upload it
to web with drag or click on upload area, webapps wil crop the particular field which is defined before and extract the in"form jobsheet"ation and then save the in"form jobsheet"ation to database.

### Database

this webapps using sqlite for store the data from respone google cloud vision API which include:

- jobsheet number
- customer name
- customer address
- model device
- serial number
- technisian name
- problem
- solution

## How to launch application

1. you need enable google cloud vision API on you google cloud plat"form jobsheet"
2. create service account it will give you a json file which include your credential to use google cloud vision api
3. run pip install -r requirements.txt to install needed libraries
4. run command flask run