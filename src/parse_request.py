from http import HTTPStatus
from select_validator import SelectValidator
import traceback
from config import Config
import hashlib
import datetime
import logging


class ParseRequest:
    def __init__(self, request):
        self.request = request
        self.method = None
        self.validation_failed_code = HTTPStatus.UNPROCESSABLE_ENTITY
        self.code = None
        self.response = None

    def check_auth(self):
        request = self.request['body']
        logging.info("check_auth. login:")
        logging.info(request.get("login"))
        if request.get("login") == Config().admin_login:
            token = hashlib.sha512((datetime.datetime.now()
                                    .strftime("%Y%m%d%H")
                                    + Config(
                    ).admin_salt).encode('utf-8')).hexdigest()
        else:
            msg = request.get("account", "") + \
                  request.get("login", "") \
                  + Config().salt
            token = hashlib.sha512(msg.encode('utf-8')).hexdigest()
        if token != request.get("token"):
            raise ValueError('invalid token')

    def _get_method(self):
        logging.info("start method_handler")
        if 'body' in self.request.keys() is False:
            raise ValueError('body is absent')
        logging.info("request type:")
        logging.info(type(self.request))
        logging.info(self.request)
        logging.info("body:")
        logging.info(self.request['body'])
        if 'method' in self.request['body'].keys() is False:
            raise ValueError('method is absent')
        self.method = self.request['body']['method']
        logging.info("finish method_handler")

    def get(self):
        try:
            self._get_method()
        except Exception as e:
            self.code = self.validation_failed_code
            self.response = str(e)
            return self.response, self.code

        try:
            self.check_auth()
        except Exception:
            self.code = HTTPStatus.FORBIDDEN
            self.response = "invalid credentials"
            logging.exception("exception:")
            return self.response, self.code

        try:
            validator = SelectValidator(self.request)
            info = getattr(validator, self.method)()
        except Exception as e:
            self.code = self.validation_failed_code
            self.response = str(e)
            info = self.response, self.code
            logging.exception("exception:")
        finally:
            return info
