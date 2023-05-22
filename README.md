## OCR handwriting "Form Jobsheet" data extractor using Python and Google Cloud Vision API
### Video Demo:  https://youtu.be/ocDpP9oc0Ko
### Description:
this webapps is using python and google cloud vision to ocr handwriting "form jobsheet". this can be used to convert the physical "form jobsheet" to digital "form jobsheet", because the function is to OCR the handwriting text to standard computer character. The accuracy google cloud vision for ocr-ing handwriting text is pretty high.

The upload folder is for hold the uploaded file "form jobsheet". The "form jobsheet" have many informations that is important for the company because it relatively to the history of the device.  app.py is the main application program, it include the route and methods for the webapps.
The app.py have two routes, index and upload,  index for handle the user interface of main page in webapps,  and upload for handle the upload proses and ocr-ing process including align uploaded image.

Technologies used:

- Google Cloud Vision API
- Flask
- opencv
- bootstrap
- jquery
- other libraries or packages

### Project Structure

project  
├── app  
│   ├── templates  
│   │   └── form_jobsheet_template.jpg  
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

### How the webapps works?

The user download "form jobsheet" template, print it and fill each field with handwriting then scan using scanner device or multi function printer which have scanner function as an image then upload it to web with drag or click on upload area, webapps wil crop the particular field which is defined before, and extract the informations and then save it to database.

### Database

this webapps using sqlite for store the data from respone google cloud vision API which include:

- jobsheet number
- customer name
- customer address
- model device
- serial number
- technician name
- problem
- solution

### How to launch application

1. You need enable google cloud vision API on you google cloud console  
    - Go to [Google Cloud Platform](https://console.cloud.google.com/apis/library/vision.googleapis.com)  
    - Click enable  
    - Create service account, it will give you a json file which include your credential to use google cloud vision api  
    - Download the json file  
    - Rename the json file to symbolic-wind.json and put it in app folder  
2. Run <code>pip install -r requirements.txt</code> to install needed libraries
3. Run <code>flask run</code>

### Contact
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/andiwinata87/)