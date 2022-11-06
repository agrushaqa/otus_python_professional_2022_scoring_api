#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import hashlib
import json
import logging
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from optparse import OptionParser

from config import Config
from parse_request import ParseRequest


def check_auth(request):
    if request.is_admin:
        digest = hashlib.sha512(datetime.datetime.now().strftime(
            "%Y%m%d%H") + Config().admin_salt).hexdigest()
    else:
        digest = hashlib.sha512(
            request.account + request.login + Config().salt).hexdigest()
    if digest == request.token:
        return True
    return False


def _get_method(request):
    logging.info("start method_handler")
    if 'body' in request.keys() is False:
        raise ValueError('body is absent')
    logging.info("request type:")
    logging.info(type(request))
    logging.info(request)
    logging.info("body:")
    logging.info(request['body'])
    if 'method' in request['body'].keys() is False:
        raise ValueError('method is absent')
    logging.info("finish method_handler")
    return request['body']['method']


def method_handler(request, ctx, store):
    logging.info("start method_handler")
    print("request:")
    print(request)
    try:
        method = _get_method(request)
    except Exception as e:
        code = Config().validation_failed_code
        response = str(e)
        return response, code

    parser = ParseRequest(request)
    return parser.get(method, ctx, store)


class MainHTTPHandler(BaseHTTPRequestHandler):
    router = {
        "method": method_handler
    }
    store = None

    def get_request_id(self, headers):
        return headers.get('HTTP_X_REQUEST_ID', uuid.uuid4().hex)

    def do_POST(self):
        response, code = {}, HTTPStatus.OK
        context = {"request_id": self.get_request_id(self.headers)}
        request = None
        try:
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            request = json.loads(data_string)
        except Exception:
            code = HTTPStatus.BAD_REQUEST

        if request:
            path = self.path.strip("/")
            logging.info(
                "%s: %s %s" % (self.path, data_string, context["request_id"]))
            if path in self.router:
                try:
                    response, code = self.router[path](
                        {"body": request, "headers": self.headers}, context,
                        self.store)
                except Exception as e:
                    logging.exception("Unexpected error: %s" % e)
                    code = HTTPStatus.INTERNAL_SERVER_ERROR
            else:
                code = HTTPStatus.NOT_FOUND

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if code not in Config().errors:
            r = {"response": response, "code": code}
        else:
            logging.info("response:")
            logging.info(response)
            r = {"error": response or Config().errors.get(code, "Unknown "
                                                                "Error"),
                 "code": code}
        context.update(r)
        logging.info(context)
        logging.info("response:")
        logging.info(r)
        self.wfile.write(bytes(json.dumps(r), "utf8"))
        return


if __name__ == "__main__":
    op = OptionParser()
    op.add_option("-p", "--port", action="store", type=int, default=8080)
    op.add_option("-l", "--log", action="store", default=None)
    (opts, args) = op.parse_args()
    logging.basicConfig(filename=opts.log, level=logging.INFO,
                        format='[%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S')
    server = HTTPServer(("localhost", opts.port), MainHTTPHandler)
    logging.info("Starting server at %s" % opts.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
