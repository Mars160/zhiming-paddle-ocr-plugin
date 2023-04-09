from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from requests import get, post

class OCR(Resource):
    OCR_URL = 'http://localhost:65533/ocr'

    @jwt_required()
    def get(self, uuid):
        req = get('{}/{}'.format(self.OCR_URL, uuid))
        return req.json()

    @jwt_required()
    def post(self):
        file = request.files['file']
        req = post(self.OCR_URL, files={'file': file})
        return req.json()

