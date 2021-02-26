from logger import Logger
from models import TrainingSite
from src.conf import code_success
from src.render import render
import datetime

site = TrainingSite()
logger = Logger('views')


def main(request):
    static = request.get('static', None)
    return code_success, render('index.html', static=static)


def courses_list(request):
    logger.log('Список курсов')
    return code_success, render('list_courses.html', objects_list=site.courses)


def copy_course(request):
    request_params = request['request_params']
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return code_success, render('list_courses.html', objects_list=site.courses)


def category_list(request):
    logger.log('Список категорий')
    return code_success, render('list_category.html', objects_list=site.categories)


def create_course(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
            course = site.create_course('record', name, category)
            site.courses.append(course)
        return code_success, render('create_course.html')
    else:
        return code_success, render('create_course.html', categories=site.categories, course=site.courses)


def create_category(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
        new_category = site.create_category(name, category)
        site.categories.append(new_category)
        return code_success, render('create_category.html', categories=site.categories)
    else:
        categories = site.categories
        return code_success, render('create_category.html', categories=categories)


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
