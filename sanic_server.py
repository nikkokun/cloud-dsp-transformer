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

import dspcore
import json
from sanic.response import json
from sanic_cors import CORS, cross_origin

import os
import os.path
import wget

import ujson

# Out audio effect library
# import dspcore
# Mock of our audio effect library (for testing/debugging)
# import dspcore_mock as dspcore


app = Sanic()
STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
url = ""
CORS(app, automatic_options=True)


### REST APIs (Public) ###

@app.route('/upload')
async def upload(request):

	filename = request.args['filename'][0]

	audio_file_url = upload_file_to_cloudinary(filename)

	return text("uploaded to cloudinary: " + audio_file_url)

@app.post('/transform')
async def transform(request):
	# Applies a transform to the specified file on the cloudinary
	# Usage:
	# - http://localhost:8000/transform?filename=song.wav&type=stretch
	# - The value for shift must be in the range [-100,100]

	#logger.info(request.body)

	data = ujson.loads(request.body)
	#logger.info(data['url'])

	if 'url' not in data:
		return response.json({'message': "missing url"}, status=401)

	cloudinary_file_url = data['url']

	if 'transforms' not in data:
		return text('You need to specify at least one transformation.')

	#transform_type = args['type'][0] if 'type' in args else 'type_not_specified'
	shift = 0
	size = 0

	# Download the specified file from cloudinary
	saved_file = download_from_cloundinary(cloudinary_file_url)

	transforms = data['transforms']


	for transform in transforms:
		transform_type = transform['type']

		if transform_type == 'stretch':
			transformed_file_path = dspcore.stretch(saved_file, 2)
		elif transform_type == 'pitch_shift':
			transformed_file_path = dspcore.pitchShift(saved_file, 4)
		elif transform_type == 'percussive':
			transformed_file_path = dspcore.percussive(saved_file,3)
		elif transform_type == 'harmonic':
			transformed_file_path = dspcore.harmonic(saved_file,3)
		elif transform_type == 'dj':
			transformed_file_path = dspcore.dj(saved_file,-4)
		else:
			print('Error: unknown transform type {}'.format(transform_type))


	upload_url = upload_file_to_cloudinary(transformed_file_path)

	if len(upload_url) == 0:
		return response.json({'message': "Failed to upload a media file"}, status=500)

	return response.json({'url': upload_url})

def upload_file_to_cloudinary(file_path):
	# Returns the URL of the file uploaded to Cloudinary

	try:
		cr = cloudinary.uploader.upload(file_path,
			overwrite = True,
			notification_url = "",
			resource_type = "auto"
			)

		return cr['url']
	except Exception as e:
		logger.error(e)
		return ""

	logger.info('uploaded to cloudinary: ' + ujson.dumps(cr))


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

	extension = os.path.splitext(url)[1]
	filename = f'file{extension}'
	print(extension)
	logger.info('downloading file from c')

	# Make sure that the work folder exists
	# See
	# https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python 
	# for in-depth discussion on this
	dir = 'downloads_from_cloudinary'
	if not os.path.exists(dir):
		os.makedirs(dir)

	output_file_path = os.path.join(dir, filename)

	# Delete if there is a previous download with the same name otherwise wget.download
	# would save a new download with a different name, e.g. song (1).wav, and old file
	# will get uploaded
	if os.path.exists(output_file_path):
		os.remove(output_file_path)

	logger.info('downloading ' + output_file_path)
	f = wget.download(url, out=output_file_path)
	logger.info('wget return value: {}'.format(f))

	return output_file_path

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

	#shift = 50

	#dspcore.pitchShift('testdata/BlueSea_A024.wav',shift,'testdata/pitch_shifted.wav')

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
