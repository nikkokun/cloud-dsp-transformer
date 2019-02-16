# Notes
# - Run this first to install dependencies
#   - pip3 install sanic wget librosa soundfile

from sanic import Sanic
from sanic import response
from sanic.response import text
from sanic.log import logger

import cloudinary
import cloudinary.uploader
import cloudinary.api

import json
import os
import wget

# Out audio effect library
#import dspcore

# Mock of our audio effect library (for testing/debugging)
import dspcore_mock as dspcore


app = Sanic()
STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
url = ""


### REST APIs (Public) ###

@app.route('/upload')
async def upload(request):

    filename = request.args['filename'][0]

    audio_file_url = upload_file_to_cloudinary(filename)

    return text("uploaded to cloudinary: " + audio_file_url)

@app.route('/pitch_shift')
async def pitchShift(request):
    # Applies a pitch shift to the specified file on the cloudinary
    # Usage:
    # - http://localhost:8000/pitch_shift?filename=song.wav&shift=50
    # - The value for shift must be in the range [-100,100]

    filename = request.args['filename'][0]
    shift = request.args['shift'][0]

    # Download the specified file from cloudinary
    download_from_cloundinary(filename)

    output_filename = 'pitch_shifted.wav'

    dspcore.pitchShift(filename,shift,output_filename)

    # 
    return text('factor: {}, filename: {}'.format(factor,filename))

@app.route('/stretch')
async def stretch(request):

    factor = request.args['factor'][0]
    filename = request.args['filename'][0]
    output_filename = filename

    return text('factor: {}, filename: {}'.format(factor,filename))

def upload_file_to_cloudinary(file_path):
    # Returns the URL of the file uploaded to Cloudinary

    cr = cloudinary.uploader.upload(file_path,
    folder = "audio_files/",
    public_id = file_path,
    overwrite = True,
    notification_url = "",
    resource_type = "auto")

    logger.info('uploaded to cloudinary: ' + json.dumps(cr))

    return cr['url']


@app.route('/download')
async def download_file(request):
    # Download a file from the cloudinary storage
    # Example:
    # - http://localhost:8000/download?filename=song.wav
    # -> Downloads the file http://res.cloudinary.com/dnh7vvs4n/video/upload/v1550255574/audio_files/song.wav

    cloudinary_folder_url = 'http://res.cloudinary.com/dnh7vvs4n/video/upload/v1550255574/audio_files/'

    filename = request.args['filename'][0]

    audio_file_url = cloudinary_folder_url + filename

    logger.info('downloading file: {}'.format(filename))

    download_from_cloundinary(audio_file_url)

    return text('downloaded file')


### Private Functions ###

def download_from_cloundinary(url):
    logger.info('downloading file from c')

    # Make sure that the work folder exists
    # See
    # https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python 
    # for in-depth discussion on this
    dir = 'downloads_from_cloudinary'
    if not os.path.exists(dir):
        os.makedirs(dir)

    output_file_path = os.path.join(dir,'file.wav')
    logger.info('downloading ' + output_file_path)
    f = wget.download(url,output_file_path)
    logger.info('wget return value: {}'.format(f))


### Test Functions ###

@app.route('/test_upload')
async def test_upload(request):

    file_url = upload_file_to_cloudinary('testdata/BlueSea_A024.wav')

    return response.json({'url': file_url})

@app.route('/test_download')
async def test_download(request):

    test_file_url = 'https://res.cloudinary.com/dnh7vvs4n/video/upload/v1550288802/audio_files/download_test_file.wav'

    download_from_cloundinary(test_file_url)

    return text('Downloaded {}'.format(test_file_url))

@app.route('/test_pitch_shift')
async def test_pitch_shift(request):
    # Usage
    # - http://localhost:8000/test_pitch_shift

    shift = 50

    dspcore.pitchShift('testdata/BlueSea_A024.wav',shift,'testdata/pitch_shifted.wav')

    return response.json({'shift': shift})

def init_server():
    logger.info('Initializing the server')

    # the static file serving is only used during debugging
    app.static('/static', STATIC_FOLDER)
    app.static('/favicon.ico', os.path.join(STATIC_FOLDER, 'img', 'favicon.ico'))

    # Auth thing (Takashi's cloudinary storage)
    logger.info('Configuring cloudinary')
    ret = cloudinary.config(
    cloud_name = "dnh7vvs4n",
    api_key = "356324651562522",
    api_secret = "H4flEf-AWZoqjy82jmj8riY6314"
    )

    # Check to see if config completed without any issues
    logger.info(str(ret))

if __name__ == '__main__':
    init_server()
    app.run(hsot='0.0.0.0', port=8000)