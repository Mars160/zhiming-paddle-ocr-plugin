from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from requests import get, post


class OCR(Resource):
    OCR_URL = 'http://localhost:65533/ocr'

    @jwt_required()
    def get(self, uuid):
        try:
            req = get('{}/{}'.format(self.OCR_URL, uuid))
            return req.json()
        except:
            return {
                "code": 500,
                "data": None,
                "msg": "OCR后端未部署"
            }

    @jwt_required()
    def post(self):
        try:
            file = request.files['file']
            req = post(self.OCR_URL, files={'file': file})
            return req.json()
        except:
            return {
                "code": 500,
                "data": None,
                "msg": "OCR后端未部署"
            }
