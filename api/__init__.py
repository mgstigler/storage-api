import logging
from flask import Flask, request, send_from_directory
from s3 import upload, download
import tempfile
import os

def create_app():
    logging.getLogger().level = logging.INFO
    app = Flask(__name__)

    @app.route('/hundred-acre/storage/download', methods=['GET'])
    def download_receipt():
        logging.log(logging.INFO, 'Downloading receipt...')
        file_name = request.headers['filename']
        bucket = os.environ['BUCKET']
        logging.log(logging.INFO, "Filename found: " + file_name)
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, file_name)
            resp = download.download_receipt(file_name, bucket, file_path)
            logging.log(logging.INFO, "receipt downloaded")
            return send_from_directory(temp_dir, file_name, as_attachment=True)

    @app.route('/hundred-acre/storage/upload', methods=['POST'])
    def upload_receipt():
        logging.log(logging.INFO, 'Uploading receipt...')
        file = request.files['file']
        filename = file.filename
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, file.filename)
            file.save(file_path)
            bucket = os.environ['BUCKET']
            resp = upload.upload_file(file_path, bucket,filename)
            if resp == True:
                logging.log(logging.INFO, "receipt uploaded")
                return "successfully uploaded", 200
            else:
                logging.log(logging.INFO, "receipt failed to upload")
                return "errors uploading file", 500

    return app