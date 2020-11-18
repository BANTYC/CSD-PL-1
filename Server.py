from werkzeug.wrappers import Request
from wsgiref.util import setup_testing_defaults, request_uri, shift_path_info
from wsgiref.simple_server import make_server
from datetime import datetime
from dateutil import parser
import wsgiref.headers
import pytz
import json
import re


# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults


def simple_app(environ, start_response):
    setup_testing_defaults(environ)

    request_method = environ['REQUEST_METHOD']
    url = request_uri(environ)
    uri = shift_path_info(environ)

    status = '200 OK'
    source = '';
    headers = [];

    if request_method == 'GET':
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        if uri == '':
            source = str(datetime.now().time())[0:8]

        else:
            tz_arg = url.split('/')[3] + '/' + url.split('/')[4]

            try:
                tz = pytz.timezone(tz_arg)
                source = str(datetime.now(tz))[11:19]
            except pytz.exceptions.UnknownTimeZoneError:
                source, status = nig(source, status)

    elif request_method == 'POST':
        headers = [('Content-type', 'application/json; charset=utf-8')]
        path = '/'
        path = path.join(url.split('/')[3:])
        if path == "api/v1/date":
            try:
                tz = pytz.timezone(read_json(environ)['tz'])
                source = str(datetime.now(tz))[0:10]
                source = source.split('-')
                source.reverse()
                source = '-'.join(source);
                source = json.dumps({'date': source})
            except pytz.exceptions.UnknownTimeZoneError:
                source, status = nig(source, status)

        elif path == "api/v1/time":
            try:
                tz = pytz.timezone(read_json(environ)['tz'])
                source = str(datetime.now(tz))[11:19]
                source = json.dumps({'time': source})
            except pytz.exceptions.UnknownTimeZoneError:
                source, status = nig(source, status)

        elif path == "api/v1/datediff":
            try:
                params = read_json(environ)
                start = parser.parse(params['start']['date'])
                end = parser.parse(params['end']['date'])

                result = ''

                if ("tz" in params['start']) & ("tz" in params['end']):
                    start_tz = pytz.timezone(params['start']['tz'])
                    end_tz = pytz.timezone(params['end']['tz'])
                    start = start_tz.localize(start)
                    end = end_tz.localize(end)
                    result = abs(end - start)

                elif "tz" in params['start']:
                    start_tz = pytz.timezone(params['start']['tz'])
                    end_tz = pytz.timezone('GMT')
                    start = start_tz.localize(start)
                    end = end_tz.localize(end)
                    result = abs(end - start)

                elif "tz" in params['end']:
                    start_tz = pytz.timezone('GMT')
                    end_tz = pytz.timezone(params['end']['tz'])
                    start = start_tz.localize(start)
                    end = end_tz.localize(end)
                    result = abs(end - start)

                else:
                    result = abs(end - start)

                source = str(result)
                source = json.dumps({'result': source})
            except:
                source, status = nig(source, status)

    start_response(status, headers)
    ret = [x.encode('utf-8') for x in source]
    return ret


def nig(source, status):
    status = '400 BAD REQUEST'
    source = ''
    return source, status


def read_json(environ):
    try:
        req_body_size = int(environ['CONTENT_LENGTH'])
    except (ValueError):
        req_body_size = 0

    req_body = environ['wsgi.input'].read(req_body_size)

    return json.loads(req_body)


def get_date(tz):
    try:
        source = str(datetime.now(tz))[11:19]
        source = json.dumps({'time': source})
    except pytz.exceptions.UnknownTimeZoneError:
        status = '400 BAD REQUEST'
        source = ''


with make_server('', 8000, simple_app) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
