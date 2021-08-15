import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename, send_file
import PyPDF2
from time import sleep
import gtts

UPLOAD_FOLDER = './static/files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "Test.pdf"))
            reader()
            return redirect(url_for('download_file', name=filename))
    return render_template('index.html')

@app.route('/templates/<name>')
def download_file(name):
    return render_template('reader.html')

def reader():
    pdfFileObj = open('static/files/Test.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(0)
    output = pageObj.extractText()
    print(output)
    tts = gtts.gTTS(output)
    filename = 'temp.mp3'
    tts.save(f'static/files/{filename}')
    # music = pyglet.media.load(filename, streaming=False)
    # music.play()

    # sleep(music.duration)  # prevent from killing
    # os.remove(filename)  # remove temperory file

@app.route('/')
def test():
    return render_template("home.html")



@app.route('/aboutpage')
def about():
    return render_template("aboutpage.html")

