import os
from threading import Thread

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from plugins.tunnel import response_base
import uuid

from .ext import *
from .ocr import *


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png']


class OCR(Resource):
    OCR_DICT = {}

    # @jwt_required()
    def get(self, uuid):
        response = response_base.copy()
        if uuid in self.OCR_DICT:
            if self.OCR_DICT[uuid] != 0:
                response['data'] = self.OCR_DICT[uuid]
                del self.OCR_DICT[uuid]
            else:
                response['data'] = None
                response['msg'] = '正在识别中...'
        else:
            response['backend'] = 404
            response['msg'] = 'OCR任务不存在'
        return response

    # @jwt_required()
    def post(self):
        response = response_base.copy()
        file = request.files['file']
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1]
            random_name = '{}'.format(uuid.uuid4().hex)
            file.save('{}{}{}'.format(TEMP_DIR, os.sep, random_name))

            # 新开一个线程来识别
            p = Thread(target=self.start_ocr, args=(random_name,))
            p.start()
            response['data'] = random_name
        return response

    def start_ocr(self, filename):
        filepath = '{}{}{}'.format(TEMP_DIR, os.sep, filename)
        self.OCR_DICT[filename] = 0
        result = ocr(filepath)
        self.OCR_DICT[filename] = result
        os.remove(filepath)
