import datetime
import hashlib
import logging
from http import HTTPStatus

from config import Config
from select_validator import SelectValidator


class ParseRequest:
    def __init__(self, request):
        self.request = request
        self.method = None
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

    def get(self, method, context, store):
        try:
            self.check_auth()
        except Exception:
            self.code = HTTPStatus.FORBIDDEN
            self.response = "invalid credentials"
            logging.exception("exception:")
            return self.response, self.code

        try:
            validator = SelectValidator(self.request)
            info = getattr(validator, method)(context, store)
        except Exception as e:
            self.code = Config().validation_failed_code
            self.response = str(e)
            info = self.response, self.code
            logging.exception("exception:")
        finally:
            return info
