from flask import Flask
app = Flask(__name__)

from flask.logging import default_handler


import json
import os
import wget

import cloudinary
import cloudinary.uploader
import cloudinary.api

@app.route('/upload')
async def upload(request):

    filename = request.args['filename'][0]
    audio_file_url = upload_file_to_cloudinary(filename)
    return ("uploaded to cloudinary: " + audio_file_url)

def upload_file_to_cloudinary(file_path):
    # Returns the URL of the file uploaded to Cloudinary

    cr = cloudinary.uploader.upload(file_path,
    folder = "audio_files/",
    public_id = file_path,
    overwrite = True,
    notification_url = "",
    resource_type = "auto")

    app.logger.info('uploaded to cloudinary: ' + json.dumps(cr))

    return cr['url']
