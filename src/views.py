from src.conf import code_success
from src.render import render


def main(request):
    static = request.get('static', None)
    return code_success, render('index.html', static=static)


def about(request):
    static = request.get('static', None)
    return code_success, render('about.html', static=static)
