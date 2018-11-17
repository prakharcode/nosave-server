from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import base64

app = Flask(__name__)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file_input' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file_input']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_data = file.stream.read()
            nparr = np.fromstring(file_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # DO YOUR IMAGE PROCESSING STUFF

            stuff = img
            img_str = cv2.imencode('.jpg', stuff)[1].tostring()
            encoded = base64.b64encode(img_str).decode("utf-8")
            mime = "image/jpg;"
            out_image = f"data:{mime}base64,{encoded}"
            return render_template('result.html', out_image = out_image)
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = "YOUR SECRET KEY"
    app.run(debug=True)
