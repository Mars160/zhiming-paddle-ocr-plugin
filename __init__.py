import os
import atexit
import shutil
from plugins.tunnel import *
from .backend.ext import *
from .backend.resource import OCR
import logging

# 如果要添加新的endpoint，建议加一个plugin前缀用于标注为插件，例如/v1/plugin/ocr
# code below this line，以下代码都会执行

# 新建临时目录
if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)


# 删除临时目录
@atexit.register
def clean():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)


api = get_global('api')
api.add_resource(OCR, '/v1/plugin/ocr', '/v1/plugin/ocr/<string:uuid>')
# 打印api的所有url
logging.info('OCR插件加载完成')
