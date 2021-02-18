from src.conf import code_success
from src.render import render
import datetime


def main(request):
    static = request.get('static', None)
    return code_success, render('index.html', static=static)


def about(request):
    static = request.get('static', None)
    return code_success, render('about.html', static=static)


def contact(request):
    # if request['method'] == 'GET':
    #     data = request['request_params']
    #     theme = data['theme']
    #     email = data['email']
    #     text = data['text']
    #
    #     msg = f'\nGET-форма\nДата: {datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}\n' \
    #           f'E-mail: {email}\n' \
    #           f'Тема: {theme}\n' \
    #           f'Сообщение: {text}\n'
    #
    #     print(msg)
    #     with open('email/emails.txt', 'a+') as f:
    #         f.write(msg)

    if request['method'] == 'POST':
        data = request['data']
        theme = data['theme']
        email = data['email']
        text = data['text']

        msg = f'\nPOST-форма\nДата: {datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}\n' \
              f'E-mail: {email}\n' \
              f'Тема: {theme}\n' \
              f'Сообщение: {text}\n'

        print(msg)

        with open('email/emails.txt', 'a+') as f:
            f.write(msg)

        return code_success, render('contacts.html')
    else:
        return code_success, render('contacts.html')
