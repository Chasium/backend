"""
后端的入口文件
"""
from http_api import http_api
from ws_api import ws_api
from db import db
import config
import config_production
import os

if os.environ.get('PRODUCTION_ENV') == 'true':
    http_api.config.from_object(config_production)
else:
    http_api.config.from_object(config)

db.init_app(http_api)
ws_api.init_app(http_api, cors_allowed_origins="*")

if __name__ == '__main__':
    ws_api.run(http_api)
