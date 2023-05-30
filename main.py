import os
import time

from flask import flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from loguru import logger

from app import app
from utils import count_people_on_video


@app.route('/')
def upload_form():
    """
    Renders the upload.html template for the root route.
    """
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_video():
    """
    Handles POST requests to the root route that contain a file to process.
    """
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No video selected for uploading')
        return redirect(request.url)
    if not file.filename.endswith('.mp4'):
        flash('File is not video')
        return redirect(request.url)
    else:
        flash('Started counting. Please, wait')
        logger.info(f'Started processing file {file.filename}')
        filename = secure_filename(file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(video_path)
        logger.info(f'Saved file {file.filename} successfully and started '
                    f'model inference on {app.config["frames_to_process"]} '
                    f'frames')
        num_people, pil_image = count_people_on_video(video_path,
                                                      app.config[
                                                          'feature_extractor'],
                                                      app.config['model'],
                                                      app.config[
                                                          'frames_to_process'])
        if os.path.exists(video_path):
            os.remove(video_path)
        img_path = os.path.join(app.config['RESULT_FOLDER'],
                                f'{int(time.time())}.jpg')
        pil_image.save(img_path)
        return render_template('result.html',
                               num_people=num_people,
                               img_name=img_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
