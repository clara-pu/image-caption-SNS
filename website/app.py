from flask import Flask, flash, request,render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import helpers
import os

images_folder = os.path.join('static','images')
allowed_extensions = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = images_folder

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['GET','POST'])
def upload():
    if request.method == "POST":
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            prediction = helpers.euclidean_predict_one_image(filepath)


    return render_template('index.html', predicted_caption = prediction, pic_path = filepath)
    
    '''
    post_name = 'cat.jpg'
    predicted_caption = post_name
    #return render_template('index.html', display_image = full_filename)

    global counter_index
    context = [ (index,message) for message,index in test_context[counter_index]]
    
    text = request.args.get('q', '')
    if text != "":
        result = auto_complete(context,text)
    else:
        result = ""

    if request.method == 'POST':
        if "new_post" in request.form:
            post_name = helpers.pick_post()
        elif "generate_caption" in request.form:
            predicted_caption = helpers.predict(post_name)

    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], post_name)
    return render_template('index.html', display_image = sfname, display_caption = predict(sfname))
    '''

    

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)