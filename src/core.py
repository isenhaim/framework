from src.conf import header, code_not_found
from src.render import render
from urllib.parse import unquote


class Application:

    def __init__(self, urlpatterns: dict, middlewares: list):
        self.urlpatterns = urlpatterns
        self.middlewares = middlewares

    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']

        method = environ['REQUEST_METHOD']
        data = self.get_input_data(environ)
        data = self.decode_input_data(data)

        query_string = environ['QUERY_STRING']
        request_params = self.parser_input_data(query_string)

        if not path.endswith('/'):
            path = f'{path}/'

            view = self.urlpatterns[path]
            request = {}

            request['method'] = method
            request['data'] = data
            request['request_params'] = request_params

            for middleware in self.middlewares:
                middleware(request)

            code, template = view(request)
            start_response(code, header)

            return [template.encode('utf-8')]

        else:
            start_response(code_not_found, header)
            template = render('404.html')
            return [template.encode('utf-8')]

    def parser_input_data(self, data: str):
        result = {}
        if data:
            data = unquote(data)
            params = data.split('&')
            for item in params:
                key, value = item.split('=')
                result[key] = value
        return result

    def decode_input_data(self, data: bytes):
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parser_input_data(data_str)
        return result

    def get_input_data(self, environ):
        length = int(environ.get('CONTENT_LENGTH', '0'))
        data = environ['wsgi.input'].read(length)
        return data
