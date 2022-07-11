import os, io

from datetime import date
from cs50 import SQL
from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from google.cloud import vision
from google.cloud import vision_v1
from collections import namedtuple
from werkzeug.utils import secure_filename
import cv2
import pandas as pd

from align_image import align_images

# Locate The json file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'app/symbolic-wind.json'
client = vision.ImageAnnotatorClient()

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure allowed file extension
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png']

# Configure path
app.config['UPLOADED_PATH'] = 'app/upload/'
app.config['DOWNLOAD_PATH'] = 'app/templates/'
form_template = 'app/templates/form_jobsheet_template.jpg'

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///static/db/ocrdata.db")

OCRLocation = namedtuple("OCRLocation", ["id", "bbox",
	"filter_keywords"])
# define the locations of each area of the document we wish to OCR
OCR_LOCATIONS = [
	OCRLocation("jobsheet_no", (2075, 205, 332, 64), []),
	OCRLocation("cust_name", (548, 490, 1856, 66), ["last", "name"]),
	OCRLocation("cust_addr", (550, 582, 1856, 66), ["address"]),
	OCRLocation("device_model", (548, 681, 749, 64), []),
	OCRLocation("serial_no", (1658, 681, 748, 64), []),
	OCRLocation("tech_name", (548, 806, 749, 63), ["employee"]),
	OCRLocation("problem", (109, 1099, 1030, 566), ["date"]),
	OCRLocation("solution", (1370, 1101, 1029, 564), []),
	OCRLocation("date", (2075, 290, 330, 63), []),
]

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route("/", methods=["GET"])
def index():
    dataforms = db.execute("SELECT * FROM dataforms")
    return render_template("index.html", dataforms=dataforms)

@app.route("/download/<path:filename>", methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(app.config['DOWNLOAD_PATH'], filename, as_attachment=True)

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get('file')
    filename = secure_filename(f.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Invalid image", 400
    file_path = os.path.join(app.config['UPLOADED_PATH'], filename)
    f.save(file_path)

    # load the input image and template from disk
    print("[INFO] loading images...")
    image = cv2.imread(file_path)
    template = cv2.imread(form_template)

    # align the images
    print("[INFO] aligning images...")
    aligned = align_images(image, template)
    file_align, ext_align = os.path.splitext(file_path)
    cv2.imwrite(f'{file_align}_align{ext_align}', aligned)
    #os.remove(file_path)

    # initialize a results list to store the document OCR parsing results
    print("[INFO] OCR'ing document...")
    parsingResults = []
    count = 0
    # loop over the locations of the document we are going to OCR
    for loc in OCR_LOCATIONS:
    	# extract the OCR ROI from the aligned image
    	(x, y, w, h) = loc.bbox
    	roi = aligned[y:y + h, x:x + w]

    	# OCR the ROI using Tesseract
    	roi_image = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    	#text = pytesseract.image_to_string(rgb)

    	# saving roi
    	print('[INFO] Saving ROI as image file...')
    	cv2.imwrite(f'{file_align}_roi_{count}{file_ext}', roi_image)

    	with io.open(f'{file_align}_roi_{count}{file_ext}', 'rb') as image_file:
    	    content = image_file.read()

    	# OCR using google cloud vision API
    	image_google_vision = vision_v1.types.Image(content=content)
    	response = client.document_text_detection(image=image_google_vision)

    	# get text
    	docText = response.full_text_annotation.text
    	parsingResults.append(docText)

    	# remove file image roi
    	print('[INFO] Deleting ROI image file...')
    	#os.remove(f'{file_align}_roi_{count}{file_ext}')
    	count += 1

    # remove file align
    print('[INFO] Deleting align image file...')
    #os.remove(f'{file_align}_align{ext_align}')

    # insert data to database
    db.execute(
        "INSERT INTO dataforms (jobsheet_no, cust_name, cust_addr, device_model, serial_no, tech_name, problem, solution, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        parsingResults[0],
        parsingResults[1],
        parsingResults[2],
        parsingResults[3],
        parsingResults[4],
        parsingResults[5],
        parsingResults[6],
        parsingResults[7],
        parsingResults[8]
    )

    return render_template("index.html")