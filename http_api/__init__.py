"""
后端所有的Http API。
具体的API由APIGen生成。
"""
from flask import Flask

http_api = Flask(__name__)

from apigen.http_api import *