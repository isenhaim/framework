from src.conf import header, code_not_found
from src.render import render


class Application:

    def __init__(self, urlpatterns: dict, middlewares: list):
        self.urlpatterns = urlpatterns
        self.middlewares = middlewares

    def __call__(self, environ, start_response):

        # Добавлено тернарное выражение для отсечения / в url
        url = environ['PATH_INFO']
        path = url[0: -1] if len(url) > 1 and url[-1] == '/' else url

        if path in self.urlpatterns:
            view = self.urlpatterns[path]
            request = {}

            for middleware in self.middlewares:
                middleware(request)

            code, template = view(request)
            start_response(code, header)

            return [template.encode('utf-8')]

        else:
            start_response(code_not_found, header)
            template = render('404.html')
            return [template.encode('utf-8')]
